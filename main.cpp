#include <iostream>
#include "pico/stdlib.h"
#include "ESP8266WiFi.h"

int main(int, char**) {
    const uint led_pin = 25;
    const uint relay_pin = 0;
    
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);
    gpio_init(relay_pin);
    gpio_set_dir(relay_pin, GPIO_OUT);

    for (int i=0; i<2; i++) {

        gpio_put(relay_pin, false);
        sleep_ms(1000);
        gpio_put(relay_pin, true);
        sleep_ms(1000);
    }
}
