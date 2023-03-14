"""
Merlin Rayner, ETS22, 22.11.2022

Version 1.0, 09.03.2022

Hardware:
- 1*ESP32_lora_Display
- 3*Widerstand 220Ohm
- 1*LEDs Gruen
- 1*LEDs Gelb
- 1*LEDs Rot
- 1*Buzzer
- 1*MQ135 Gassensor
- 1*Breadboard
- Verdrahtungsbruecken

- Gassensor = Pin 36
- Led Grün = Pin 13
- Led Gelb = Pin 17
- Led Rot = Pin 23
- Buzzer = Pin 39

Bibliotheken:
- machine (integriert in Micropython)
- time (integriert in Micropython)
- math (integriert in Micropython)
- json (integriert in Micropython)
- network (integriert in Micropython)
- MQTTClient (integriert in Micropython)
"""
from funktionen import ppm_json
from funktionen import luft_gut
from funktionen import luft_mittel
from funktionen import luft_schlecht

#---------------------------- Programm --------------------------------
while True:
    # Den Analogwert vom Sensor lesen
    ppm = analog.read()
    # JSON-Funktion ausführen
    ppm_json()
    
    # Wenn der PPM-Wert unter 1000 liegt, die gute Luftqualität Funktion verwenden
    if ppm <= 1000:
        luft_gut()
    # Wenn der PPM-Wert zwischen 1000 und 1599 liegt, die mittlere Luftqualität Funktion verwenden
    if ppm >= 1000 and ppm <=1599:
        luft_mittel()
    # Wenn der PPM-Wert unter 1000 liegt, die schlechte Luftqualität Funktion verwenden
    if ppm >= 1600:
        luft_schlecht()
    
    # Jede Sekunde den Wert aktualisieren
    time.sleep(1)