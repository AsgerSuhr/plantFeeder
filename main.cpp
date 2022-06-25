#include <stdio.h>
#include <cstring>
#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "lib/esp8266.cpp"

int main() {
    esp8266_init();
    while (!ESPready) {};
    esp8266_set_mode("STA");
    connectToAP("WiFimodem-7D90", "zwy3uznxkd");
    
    // OK, all set up.
    while (1)
        tight_loop_contents();
}

