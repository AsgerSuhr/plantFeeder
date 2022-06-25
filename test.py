import picoESP8266 as esp8266
try:
    import usocket as socket
except:
    import socket
import network

SSID = 'WiFimodem-7D90'
PWD = 'zwy3uznxkd'

esp = esp8266.Esp8266(SSID, PWD)
esp.blink()
esp.setMode('Station')
esp.WiFiConnect()
