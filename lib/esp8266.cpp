#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/irq.h"
#include <string>

#define UART_ID uart0
#define BAUD_RATE 115200
#define DATA_BITS 8
#define STOP_BITS 1
#define PARITY    UART_PARITY_NONE
#define LED_PIN 25

// We are using pins 0 and 1, but see the GPIO function select table in the
// datasheet for information on which other pins can be used.
#define UART_TX_PIN 0
#define UART_RX_PIN 1

bool ESPready = false;

void on_uart_rx() {
    
    while (uart_is_readable(UART_ID)) {
        uint8_t ch = uart_getc(UART_ID);
        if (ch == '\n') {
            gpio_put(LED_PIN, 0);
            ESPready = true;
        } else {
            gpio_put(LED_PIN, 1);
            ESPready = false;
        }
        /*
        if (uart_is_writable(UART_ID)) {
            // to show communication with the esp8266 module,
            // we'll blink the picos LED when it's recieving anything, 
            // but a new line character
            if (ch == '\n') {
                gpio_put(LED_PIN, 0);
                ESPready = true;
            } else {
                gpio_put(LED_PIN, 1);
                ESPready = false;
            }
        }*/
    }
        
}

bool esp8266_init() {
    
    // Set up our UART with a basic baud rate.
    uart_init(UART_ID, 2400);

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    // Set the TX and RX pins by using the function select on the GPIO
    // Set datasheet for more information on function select
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    // Actually, we want a different speed
    // The call will return the actual baud rate selected, which will be as close as
    // possible to that requested
    int __unused actual = uart_set_baudrate(UART_ID, BAUD_RATE);

    // Set UART flow control CTS/RTS, we don't want these, so turn them off
    uart_set_hw_flow(UART_ID, false, false);

    // Set our data format
    uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);

    // Turn off FIFO's - we want to do this character by character
    uart_set_fifo_enabled(UART_ID, false);

    // Set up a RX interrupt
    // We need to set up the handler first
    // Select correct interrupt for the UART we are using
    int UART_IRQ = UART_ID == uart0 ? UART0_IRQ : UART1_IRQ;

    // And set up and enable the interrupt handlers
    irq_set_exclusive_handler(UART_IRQ, on_uart_rx);
    irq_set_enabled(UART_IRQ, true);

    // Now enable the UART to send interrupts - RX only
    uart_set_irq_enables(UART_ID, true, false);

    while (!ESPready) {}

    return true;
}

// makes sure to send the desired message to the ESP8266
// with carriage return (CR) and new line (NL)
void msgESP(std::string message) {
    // adding CR and NL to the string 
    message = message + "\r\n";
    uint8_t buflen = message.length();
    uart_write_blocking(UART_ID, message, buflen);
    //uart_puts(UART_ID, message.c_str());
}

// Basic AT commands
// Test AT startup (AT)
void AT(){

}

// restart the module (AT+RST)
void reset(){

}

// checks version information (AT+GMR)
void version(){

}

// go to deep sleep (AT+GSLP)
void deepsleep(){
    
}
void echo(){

}
/*
void restore(); // restores the factory default settings (AT+RESTORE)
void currentUART(); // current UART configuration (AT+UART CUR)
void defaultUART(); // default UART configuration saved in flash (AT+UART DEF)
void sleepMode(); // set the sleep mode (AT+SLEEP)
void checkRAM(); // checks the ramining space of ram (AT+SYSRAM)
void setMSGformat(); // set the message format (AT+SYSMSG)
void repower(); // set RF TX power (AT+REPOWER)
void configureLightSleep(); // configure light sleep wakeup source (AT+SYSLSPCFG)
void lightSleep(); // enter light-sleep mode (AT+SYSLSP)
*/

// Wi-Fi functions
// set mode to STA, AP or STA+AP (STA = station, AP = Acces Point) (AT+CWMODE)
void esp8266_set_mode(std::string mode) {
    std::string message;

    if (mode == "STA") {
        message = "AT+CWMODE=1";
    } else if (mode == "AP") {
        message = "AT+CWMODE=2";
    } else if (mode == "STA+AP") {
        message = "AT+CWMODE=3";
    } else {
        message = "AT+CWMODE=0";
    }
    
    msgESP(message);
    while (!ESPready) {}
} 

// connect to router (AT+CWJAP)
void connectToAP(std::string ssid, std::string pwd) {
    msgESP("AT+CWJAP="+'"'+ssid+'"'+','+'"'+pwd+'"');
} 
/*
void listAvailableAPs(); // list available routers in the area (AT+CWLAP)
void disconnectFromAP(); // disconnect from the router (AT+CWQAP)

//TCP/IP-related
void status(); // get current connection status (AT+CIPSTATUS)
void connect(); // establish TCP/UDP/SSL connection (AT+CIPSTART)
void send(); // send data (AT+CIPSEND)
void close(); // close connection (AT+CIPCLOSE)
void localIP(); // gets the local IP adress (AT+CIFSR)
void multiConnection(); // Configures the multiple connection mode (AT+CIPMUX)
void server(); // create or delete TCP/SSL server (AT+CIPSERVER)
void maxConnCount(); // set the maximum connections allowed by server (AT+CIPSERVERMAXCONN)
void configTransMode(); // configure transmission mode (AT+CIPMODE)
void ping(); // ping (AT+PING)
*/