import time, ujson, urequests
from machine import Pin, time_pulse_us

DEVICE_LABEL = "distance-meter"
UBIDOTS_BROKER = "industrial.api.ubidots.com"
UBIDOTS_PORT = 1883
UBIDOTS_USER = "BBUS-sPF7jmwdaxI21mnoBOdmgJA4peUtNa"
UBIDOTS_TOPIC = "/v2.0/devices/"+DEVICE_LABEL

print("Menyambungkan ke MQTT server... ", end="")
client = MQTTClient(DEVICE_LABEL, UBIDOTS_BROKER,
                    UBIDOTS_PORT, user=UBIDOTS_USER, password="")
client.connect()
print("Tersambung!")

SOUND_SPEED = 0.034

trigger = Pin(12, Pin.OUT)
echo = Pin(14, Pin.IN)


def get_distance():
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    pulse_duration = time_pulse_us(echo, 1)

    distance = pulse_duration * SOUND_SPEED / 2
    return distance


while True:
    distance = get_distance()
    status = ""
    if distance > 200:
        status = "Jauh"
    elif distance > 100:
        status = "Dekat"
    else:
        status = "Sangat Dekat"
    data = {
        "distance": {
            "value": distance,
            "context": {
                "status": status
            }
        }
    }
    
    print(f"Distance: {distance}cm, Status: {status}")
    client.publish(UBIDOTS_TOPIC, ujson.dumps(data))
    response = urequests.post("http://192.168.0.134:5000/distance/", json=data)9
    print(response.json().get('message'))
    time.sleep(5)
