from machine import UART
import time, _thread, re
from machine import Pin
import utime as time
from utils import *


class Client():
    def __init__(self, client_id, data, parentESP) -> None:
        self.esp = parentESP
        self.id = client_id
        self.data = data
        print('Client connected')
        print(self.data)
    
    def send(self, http_data:str) -> None:
        self.esp.uartSend(f'AT+CIPSEND={self.id},{str(len(http_data))}', delay=1)
        self.esp.uartSend(http_data, delay=1)
        
    def close(self) -> None:
        self.esp.uartSend(f'AT+CIPCLOSE={self.id}', delay=4)
        self.esp.client = None
        print('client closed')
    
    def GETrequest(self):
        '''returns [GET, request, HTTP protocol]'''
        return self.data[0].split(' ')

class Esp8266():
    def __init__(self, uart_id=0, baud_rate=115200, led=25) -> None:
        #super().__init__(uart_id, baud_rate)
        self.LED_pico = Pin(led, Pin.OUT)
        self.uart = UART(uart_id, baud_rate)
        self.client = None
        self.uart_id = uart_id
        self.baud_rate = baud_rate
        
    def route(self, *args):
        def wrapper(*args):
            print('start')
            f()
            print('ended')
        
    def blink(self, amount=1, delay=0.5) -> None:
        '''blinks the LED on the pico'''
        for i in range(amount):
            self.LED_pico.value(1)
            time.sleep(delay)
            self.LED_pico.value(0)
            time.sleep(delay)
            
    def setMode(self, mode:str) -> None:
        '''Sets the esp device WiFi connection mode'''
        if mode == 'NULL':
            mode = '0'
        elif mode == 'Station':
            mode = '1'
        elif mode == 'SoftAP':
            mode = '2'
        elif mode == 'SoftAP+Station':
            mode = '3'
            self.uartSend(f'AT+CWMODE={mode}', delay=2)
            self.uartSend(f'AT+CWSAP="pos_softAP","",1,0,3', delay=2)
            return

        self.uartSend(f'AT+CWMODE={mode}', delay=2)
    
    def WiFiConnect(self, ssid:str, pwd:str) -> None:
        '''connects to the wifi'''
        self.SSID = ssid 
        self.PSSW = pwd
        if self.SSID in self.uartSend('AT+CWJAP?'):
            self.uartSend(f'AT+CIFSR', delay = 1)
            return 
        else:
            self.uartSend(f'AT+CWJAP="{self.SSID}","{self.PSSW}"', delay = 10)
            self.uartSend(f'AT+CIFSR', delay = 1)
    
    def enableMultipleConnections(self, enable=True) -> None:
        '''enable multiple connections to the pico'''
        if enable:
            #enable multi connection mode
            res = self.uartSend('AT+CIPMUX=1', delay=1)
            self.blink(amount=2)
        else:
            #disable multi connection mode
            res = self.uartSend('AT+CIPMUX=0', delay=1)
            self.blink(amount=1)

    def postHTTP(self, message, ip_adress, port):
    
        # clearing the log file
        writeLog('', 'w', filename='HttpPostLog')
        
        # Establishing TCP connection
        res = self.uartSend(f'AT+CIPSTART=0,"TCP",{ip_adress},{port}', delay=4)
        writeLog(res, 'a', filename='HttpPostLog')

        # Create HTTP POST request and send it to the server
        val = f'POST / HTTP/1.1\r\nHost: 192.168.0.38\r\nUser-Agent: Mozilla\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(message)}\r\n\r\n{message}'

        # Tell the esp8266 we want to send data through the TCP connection. 0 is the ID of the connection that we established earlier
        res = self.uartSend('AT+CIPSEND=0,' + str(len(val)), delay=5)
        writeLog(res, 'a', filename='HttpPostLog')

        # Now we give the esp8266 the data
        res = self.uartSend(val, delay=10)
        writeLog(res)
        self.blink(10, delay=0.1)

        # We try and close the connection
        res = self.uartSend('AT+CIPCLOSE=0', delay=4)
        writeLog(res, 'a', filename='HttpPostLog')

    def clientHandler(self) -> None:
        while True:
            if self.uart.any():
                res = self.uart.read()
                res = res.decode('utf-8')
                #res = self.uartSerialRxMonitor()
                # Client connects
                if '+IPD' in res:
                    self.blink()
                    data = res.split('+IPD,')[-1]
                    client_id, data = data.split(',', 1)
                    data = data.split('\r\n')
                    self.client = Client(client_id, data, self)                
    
    def clientConnecting(self):
        if self.client:
            return self.client
        else:
            return None

    def server(self, port:int) -> None:
        self.enableMultipleConnections()
        res = self.uartSend(f'AT+CIPSERVER=1,{port}', delay=1)
        _thread.start_new_thread(self.clientHandler, ())
        
    def uartSerialRxMonitor(self) -> str:
        recv=bytes()
        while self.uart.any()>0:
            recv+=self.uart.read(1)
        try:
            res=recv.decode('utf-8')
        except:
            print('Error deccoding, continuing...')
            return 'ERROR'
        return res

    def uartSend(self, command:str, delay:int=1) -> str:
        self.uart.write(command+'\r\n')
        time.sleep(delay)
        res=self.uartSerialRxMonitor()
        return res