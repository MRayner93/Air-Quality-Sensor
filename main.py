import machine
import time

# Konfiguration des MQ135 Sensors
pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
RL_VALUE = 20000  # Widerstand des Lastwiderstands
RO_CLEAN_AIR_FACTOR = 3.8  # Empirischer Faktor zur Berechnung des Widerstands des Sensors bei sauberer Luft

# Funktion zur Berechnung des Widerstands des Sensors
def get_sensor_resistance():
    value = 0
    for i in range(200):
        value += pin.value()
        time.sleep_ms(1)
    value = (value/200) * 3.3 / 4096.0  # Berechnung der Spannung
    sensor_volt = value / (1.0 - value/3.3) * RL_VALUE  # Berechnung der Spannung am Sensor
    sensor_resistance = sensor_volt / RO_CLEAN_AIR_FACTOR  # Berechnung des Widerstands des Sensors
    return sensor_resistance

# Endlosschleife zum Ausgeben der Werte
while True:
    sensor_resistance = get_sensor_resistance()
    print("MQ135 Sensor Widerstand: {:.2f} kOhm".format(sensor_resistance/1000))
    time.sleep(1)
