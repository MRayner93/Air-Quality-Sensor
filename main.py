"""
Author: Merlin Rayner
Version: 1.6
"""
#-------------------------- Libraries ------------------------------
# Pins, SoftI2C, and analog pins
from machine import Pin, ADC, SoftI2C
# Time functions
import time
# JSON data format
import json
# MQTT client
from umqtt.simple import MQTTClient
# Network functions
import network
# OLED screen
import ssd1306

#------------------------ Pin Initialization --------------------------
# Green LED on Pin 22
ledGreen = Pin(22, Pin.OUT)
# Yellow LED on Pin 23
ledYellow = Pin(23, Pin.OUT)
# Red LED on Pin 17
ledRed = Pin(17, Pin.OUT)
# Buzzer on Pin 12
buzzer = Pin(12, Pin.OUT)
# I2C clock on Pin 15 - OLED
softi2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
# I2C data on Pin 4 - OLED
softi2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
# Display Reset on Pin 16 - OLED
displayReset = Pin(16, Pin.OUT)
# Sensor analog value on Pin 36
analogValue = ADC(Pin(36))

#------------------------ Analog Pin Attenuation -----------------------
# Analog Digital Converter attenuation by 11 dB
analogValue.atten(ADC.ATTN_11DB)

#------------------------ Display Initialization ----------------------
# Create I2C object
softi2c = SoftI2C(scl=softi2c_scl, sda=softi2c_sda)
# Set OLED Display Reset pin to 0
displayReset.value(0)
# Wait for 0.2 seconds
time.sleep(0.2)
# Set OLED Display Reset pin to 1
displayReset.value(1)
# Create display object and set display size
display = ssd1306.SSD1306_I2C(128, 64, softi2c)

#----------------------- LED and Buzzer Test -------------------------
# Buzzer and all LEDs turn on
buzzer.on()
ledGreen.on()
ledYellow.on()
ledRed.on()
# Wait for 0.2 seconds
time.sleep(0.2)
# Buzzer and all LEDs turn off
ledGreen.off()
ledYellow.off()
ledRed.off()
buzzer.off()

#-------------------------- Wi-Fi Connection ---------------------------
# Display Wi-Fi initialization on the OLED
display.fill(0)
display.text("Initializing", 0, 0)
display.text("Wi-Fi...", 0, 15)
display.show()

# Wi-Fi Name
WIFI_SSID = "BZTG-IoT"
# Wi-Fi Password
WIFI_PASSWORD = "WerderBremen24"
# Create Wi-Fi client
wlan = network.WLAN(network.STA_IF)
# Turn off Wi-Fi
wlan.active(False)
# Turn on Wi-Fi
wlan.active(True)
# Wait for Wi-Fi to be enabled
time.sleep(0.5)
# Connect to Wi-Fi
wlan.connect(WIFI_SSID, WIFI_PASSWORD)
# Wait for connection to be established
while not wlan.isconnected():
    pass

# Display connection success on the OLED
display.fill(0)
display.text("Successful!", 0, 0)
display.show()
time.sleep(2)

# Print SSID, IP, and Subnet mask in the console
networkList = wlan.ifconfig()
print("SSID:", wlan.config("essid"))
print("IP:", networkList[0])
print("SUBNET:", networkList[1])

#------------------------------ MQTT ----------------------------------
# Display MQTT initialization on the OLED
display.fill(0)
display.text("Initializing", 0, 0)
display.text("MQTT...", 0, 15)
display.show()

# MQTT Broker
MQTT_SERVER = "192.168.1.151"
# MQTT Client ID
CLIENT_ID = "MQTT_MR"
# MQTT Parameters
mqttClient = MQTTClient(CLIENT_ID, MQTT_SERVER, port=1883, user=None, password=None, keepalive=3600, ssl=False, ssl_params={})
# Wait for 0.5 seconds
time.sleep(0.5)
# Connect to MQTT
mqttClient.connect()

# Display connection success on the OLED
display.fill(0)
display.text("Successful!", 0, 0)
display.show()
time.sleep(2)

#----------------------------- Functions ------------------------------
# Good Air Quality Function
def airGood():
    # Green LED is on, all others off, and buzzer is silent
    ledGreen.on()
    ledYellow.off()
    ledRed.off()
    buzzer.off()
    # Display PPM and air quality on OLED
    display.fill(0)
    display.text("-Air Quality-", 7, 0)
    display.text("Good", 43, 15)
    display.text(f"PPM: {ppm}", 0, 55)
    display.show()

# Moderate Air Quality Function
def airModerate():
    # Yellow LED is on, all others off, and buzzer is silent
    ledGreen.off()
    ledYellow.on()
    ledRed.off()
    buzzer.off()
    # Display PPM and air quality on OLED
    display.fill(0)
    display.text("-Air Quality-", 2, 0)
    display.text("Moderate", 43, 15)
    display.text("!Please Ventilate!", 5, 35)
    display.text(f"PPM: {ppm}", 0, 55)
    display.show()

# Poor Air Quality Function
def airPoor():
    # Red LED is on, all others off, and buzzer beeps
    ledGreen.off()
    ledYellow.off()
    ledRed.on()
    buzzer.on()
    # Display PPM and air quality on OLED
    display.fill(0)
    display.text("-Air Quality-", 0, 0)
    display.text("Poor", 36, 15)
    display.text("!Ventilate Immediately!", 0, 35)
    display.text(f"PPM: {ppm}", 0, 55)
    display.show()
   
# JSON Function
def ppmJSON():
    # Convert sensor data to strings and write values to a dump
    sensorValue = {"AnalogValue": str(ppm)}
    output = json.dumps(sensorValue)
    # Send values to the broker - (TOPIC, PAYLOAD)
    mqttClient.publish("MQ135_AnalogValue", output)

#---------------------------- Program --------------------------------
while True:
    # Read analog value from the sensor
    ppm = analogValue.read()
    # Uncomment the next line for testing purposes if the sensor needs time to warm up
    # ppm = ppm // 2
    # Execute JSON function
    ppmJSON()
    # If PPM value is below 1000, use the good air quality function
    if ppm <= 1000:
        airGood()
    # If PPM value is between 1000 and 1599, use the moderate air quality function
    if 1000 <= ppm <= 1599:
        airModerate()
    # If PPM value is above 1600, use the poor air quality function
    if ppm
        airPoor()
    # Update the value every second
    time.sleep(1)