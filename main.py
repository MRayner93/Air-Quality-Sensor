"""
Merlin Rayner, ETS22, 22.11.2022

Version 1.5b, 12.04.2023
Neue Versionen und weitere Informationen gibt es hier: https://github.com/MRayner93/air_quality

Dieses Programm ist für einen Sensor, der die Luftqualität messen kann. Auf dem OLED Display und über das Node-Red
Dashboard wird der aktuelle Wert in ppm (Parts per Million) angezeigt. Der Sensor muss, um optimal zu funktionieren,
für mehrere Stunden aufgeheizt werden. Außerdem kann ein Ampelsystem und ein Buzzer über den Microcontroller
angesteuert werden. Bei guter Luftqualität leuchtet die grüne LED, bei mittlerer nur die gelbe LED und bei schlechter
Luftqualität leuchtet die rote LED und der Buzzer schlägt Alarm.

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
- Led Grün = Pin 22
- Led Gelb = Pin 23
- Led Rot = Pin 17
- Buzzer = Pin 12

Bibliotheken:
- machine (integriert in Micropython)
- time (integriert in Micropython)
- json (integriert in Micropython)
- network (integriert in Micropython)
- MQTTClient (integriert in Micropython)
- SSD1306 (https://github.com/stlehmann/micropython-ssd1306)
"""
#-------------------------- Bibliotheken ------------------------------
# PINs, SoftI2C und analoge PINs
from machine import Pin, ADC, SoftI2C
# Zeitfunktionen
import time
# JSON Datenformat
import json
# MQTT-Client
from umqtt.simple import MQTTClient
# Netzwerkfunktion
import network
# OLED-Screen
import ssd1306

#------------------------ Pin initialisierung --------------------------
# grüne LED auf Pin 22
ledGruen = Pin (22, Pin.OUT)
# gelbe LED auf Pin 23
ledGelb = Pin (23, Pin.OUT)
# rote LED auf Pin 17
ledRot = Pin (17, Pin.OUT)
# Buzzer auf Pin 12
buzzer = Pin (12, Pin.OUT)
# I2C-Takt auf Pin 15 - OLED
softi2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
# I2C-Daten auf Pin 4 - OLED
softi2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
# Display Reset auf Pin 16 - OLED
displayReset = Pin(16,Pin.OUT)
# Analogwert vom Sensor auf Pin 36
analogWert = ADC(Pin(36))

#------------------------ Analog Pin Verstärkung -----------------------
# Analog Digital Converter Verstärkung um 11 dB
analogWert.atten(ADC.ATTN_11DB)

#------------------------ Display initialisierung ----------------------
# I2C-Objekt wird erstellt
softi2c = SoftI2C(scl=softi2c_scl, sda=softi2c_sda)
# OLED-Display Reset-Pin wird auf 0 gesetzt
displayReset.value(0)
# Es wird 0.2 Sekunden gewartet
time.sleep(0.2)
# OLED-Display Reset-Pin wird auf 1 gesetzt
displayReset.value(1)
# Display-Objekt wird erstellt und die Größe des Displays wird festgelegt
display = ssd1306.SSD1306_I2C(128, 64, softi2c)

#----------------------- LED und Buzzer Testen -------------------------
# Buzzer und alle LEDs gehen an
buzzer.on()
ledGruen.on()
ledGelb.on()
ledRot.on()

# Es wird 0.2 Sekunden gewartet
time.sleep(0.2)

# Buzzer und alle LEDs gehen aus
ledGruen.off()
ledGelb.off()
ledRot.off()
buzzer.off()

#-------------------------- WLAN Verbindung ---------------------------
# Auf dem Display wird die Initialisierung für das WLAN angezeigt
display.fill(0)
display.text("Initialisiere", 0, 0)
display.text("WLAN...", 0, 15)
display.show()

# WLAN-Name
WIFI_SSID = "XXX"
# WLAN-Passwort
WIFI_PASSWORD = "XXX"
# WLAN-Client erzeugen
wlan = network.WLAN(network.STA_IF)
# WLAN ausschalten
wlan.active(False)
# WLAN einschalten
wlan.active(True)
# Warten, damit WLAN eingeschaltet ist
time.sleep(0.5)
# Verbindung zum WLAN herstellen
wlan.connect(WIFI_SSID,WIFI_PASSWORD)
# Solange warten, bis Verbindung hergestellt
while not wlan.isconnected():
    pass

# Auf dem Display wird der Erfolg der Verbindung angezeigt
display.fill(0)
display.text("Erfolgreich!", 0, 0)
display.show()
time.sleep(2)

# In der Konsole werden SSID, IP und die Subnetzmaske angezeigt
networkList = wlan.ifconfig()
print("SSID:", wlan.config("essid"))
print("IP:", networkList[0])
print("SUBNET:", networkList[1])

#------------------------------ MQTT ----------------------------------
# Auf dem Display wird die Initialisierung für MQTT angezeigt
display.fill(0)
display.text("Initialisiere", 0, 0)
display.text("MQTT...", 0, 15)
display.show()

# MQTT Broker
MQTT_SERVER = "XXX"
# MQTT Client ID
CLIENT_ID = "MQTT_MR"
# MQTT Parameter
mqttClient = MQTTClient(CLIENT_ID, MQTT_SERVER, port=1883, user=None, password=None, keepalive=3600, ssl=False, ssl_params={})
# 0.5 Sekunde warten
time.sleep(0.5)
# Verbinden mit MQTT
mqttClient.connect()

# Auf dem Display wird der Erfolg der Verbindung angezeigt
display.fill(0)
display.text("Erfolgreich!", 0, 0)
display.show()
time.sleep(2)
#----------------------------- Funktionen ------------------------------
# Gute Luftqualität-Funktion
def luftGut():
# Die grüne LED ist an, alle anderen aus und der Buzzer macht kein Geräusch
    ledGruen.on()
    ledGelb.off()
    ledRot.off()
    buzzer.off()
# Auf dem Display wird die PPM und die Luftqualität angezeigt
    display.fill(0)
    display.text("-Luftqualitaet-", 7, 0)
    display.text("Gut", 43, 15)
    display.text(f"PPM: {ppmAnzeige}", 0, 55)
    display.show()

# Mittlere Luftqualität-Funktion
def luftMittel():
# Die gelbe LED ist an, alle anderen aus und der Buzzer macht kein Geräusch
    ledGruen.off()
    ledGelb.on()
    ledRot.off()
    buzzer.off()
    display.fill(0)
# Auf dem Display wird die PPM und die Luftqualität angezeigt
    display.text("-Luftqualitaet-", 2, 0)
    display.text("Mittel", 43, 15)
    display.text("!Bitte Lueften!", 5, 35)
    display.text(f"PPM: {ppmAnzeige}", 0, 55)
    display.show()

# Schlechte Luftqualität-Funktion
def luftSchlecht():
# Die rote ist LED an, alle anderen aus und der Buzzer macht ein Geräusch
    ledGruen.off()
    ledGelb.off()
    ledRot.on()
    buzzer.on()
# Auf dem Display wird die PPM und die Luftqualität angezeigt
    display.fill(0)
    display.text("-Luftqualitaet-", 0, 0)
    display.text("Schlecht", 36, 15)
    display.text("!Sofort Lueften!", 0, 35)
    display.text(f"PPM: {ppmAnzeige}", 0, 55)
    display.show()
   
# JSON-Funktion
def ppmJSON():
    # Sensordaten in Strings umwandeln und die Werte in einen Dump schreiben
    sensorWert = {"Analogwert" : str(ppmAnzeige)}
    ausgabe = json.dumps(sensorWert)
    # Werte zum Broker schicken - (TOPIC, PAYLOAD)
    mqttClient.publish("MQ135_Analogwert", ausgabe)

#---------------------------- Programm --------------------------------
while True:
    # Den Analogwert vom Sensor lesen
    ppm = analogWert.read()
    # Analogwert wird zu Testzwecken durch 2 geteilt, da der Sensor meherere Stunden aufgeheizt werden muss
    ppm = ppm / 2
    # Der Analogwert wird für Node-Red und das Display auf eine ganze Zahl gerundet
    ppmAnzeige = round(ppm)
    # JSON-Funktion ausführen
    ppmJSON()
    # Wenn der PPM-Wert unter 1000 liegt, die gute Luftqualität Funktion verwenden
    if ppm <= 1000:
        luftGut()
    # Wenn der PPM-Wert zwischen 1000 und 1599 liegt, die mittlere Luftqualität Funktion verwenden
    if ppm >= 1000 and ppm <=1599:
        luftMittel()
    # Wenn der PPM-Wert unter 1000 liegt, die schlechte Luftqualität Funktion verwenden
    if ppm >= 1600:
        luftSchlecht()
    # Jede Sekunde den Wert aktualisieren
    time.sleep(1)