#include <iostream>
#include "pico/stdlib.h"

int main(int, char**) {
    const uint led_pin = 25;
    const uint relay_pin = 0;
    
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    while (true) {

        gpio_put(led_pin, true);
        sleep_ms(1000);
        gpio_put(led_pin, false);
        sleep_ms(1000);
    }
}
