# Air Quality Monitor with ESP32 and OLED Display

This program allows you to measure air quality using an MQ135 gas sensor and display the results on an OLED display. Additionally, the current value in ppm (Parts per Million) is displayed on the Node-Red dashboard. The program also controls a traffic light system and a buzzer via the microcontroller. In case of good air quality, the green LED lights up; for moderate quality, only the yellow LED lights up, and for poor air quality, the red LED lights up and the buzzer sounds an alarm.

## Table of Contents

1. [Hardware](#Hardware)
2. [Wiring](#Wiring)
3. [Libraries](#Libraries)
4. [Images](#Images)
5. [Installation](#Installation)
6. [Usage](#Usage)
7. [License](#license)


## Hardware

    1 * ESP32_Lora_Display
    3 * Resistor (220 Ohm)
    1 * 5mm LED Green
    1 * 5mm LED Yellow
    1 * 5mm LED Red
    1 * Buzzer
    1 * MQ135 Gas Sensor
    1 * Breadboard
    Jumper wires

## Wiring

    Gas Sensor: Pin 36
    LED Green: Pin 22
    LED Yellow: Pin 23
    LED Red: Pin 17
    Buzzer: Pin 12

<img src="/images/blockdiagram.png" alt="Image of the blockdiagram," width="900" height="300">

## Libraries

    machine
    time
    json
    network
    MQTTClient 
    SSD1306

## Installation

    Install Micropython on your ESP32.
    Download and install the SSD1306 library from [GitHub](https://github.com/stlehmann/micropython-ssd1306) on your ESP32.  
    Upload the program to your ESP32 and wire the hardware according to the provided wiring.
    Change the Wifi-Settings to your Network.
    Install MQTT or another Databroker and change the IP.

## Usage

Start the program on the ESP32 to monitor air quality. The current values will be displayed on the OLED display, and you can track the values in real-time via the Node-Red dashboard.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the code.

