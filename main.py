"""
Merlin Rayner, ETS22, 22.11.2022

Version 1.0, 09.03.2022

Hardware:
- 1*ESP32_lora_Display
- 3*Widerstand 220Ohm
- 1*LEDs Gruen
- 1*LEDs Gelb
- 1*LEDs Rot
- 1*MQ135 Gassensor
- 1*Breadboard
- Verdrahtungsbruecken

Gassensor = Pin 36
Led Rot = Pin 13
Led Gelb =
Led Grün =

Bibliotheken:
-machine (integriert in Micropython)
-time (integriert in Micropython)
-math (integriert in Micropython)
"""
#-------------------------- Bibliotheken ------------------------------
from machine import Pin, ADC
import time
#---------------------------- Programm --------------------------------
while True:
    adc = ADC(Pin(36))
    adc.atten(ADC.ATTN_11DB) # Einstellen des ADC-Verstärkungsfaktors auf 11 dB

    # Lesen Sie den analogen Wert
    analogwert = adc.read()

    # Drucken Sie den Wert auf der Konsole
    print(analogwert)
    
    # Umwandeln des Analogwerts in eine Spannung
   # spannung = analogwert * 0.0078125

    # Drucken Sie die Spannung auf der Konsole
   # print(spannung)
    time.sleep(1)