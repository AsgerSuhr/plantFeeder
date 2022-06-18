#include <stdio.h>
#include <cstring>
#include "pico/stdlib.h"
#include "hardware/uart.h"

#define UART_ID uart0 
#define BAUD_RATE 115200
#define LED_PIN 25
#define UART_TX_PIN 0
#define UART_RX_PIN 1

int main() {
    // Set up uart with the right baud rate, ESP8266 default is 115200
    uart_init(UART_ID, BAUD_RATE);

    //Set the GPIO pins function to be UART
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    //You can use printf to send out data through the uart, 
    //but there are other functions like:
    
    // Send out character without any conversion
    //uart_putc_raw(UART_ID, 'A');

    // Send out character but do CR/LF conversions
    //uart_putc(UART_ID, 'A');

    // Send out string with CR/LF conversion
    //uart_puts(UART_ID, "AT");


    char buffer[1024];
    //sleep_ms(10000);

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    
    while (true) {
        uart_puts(UART_ID, "AT\r\n");
        sleep_ms(10000);
    }
}
