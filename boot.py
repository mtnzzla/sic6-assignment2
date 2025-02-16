import network
import time
from umqtt.simple import MQTTClient

SSID = 'Wokwi-GUEST'
PWD = ''

print("Menyambungkan WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PWD)
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(1)
print(" Tersambung!")