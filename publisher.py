# publisher.py
import time
import random
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"   # HiveMQ public broker
PORT = 1883
TOPIC = "sensors/data"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    temperature = round(random.uniform(20.0, 45.0), 2)
    humidity = round(random.uniform(40.0, 90.0), 2)

    payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
    client.publish(TOPIC, payload)
    print(f"Published: {payload}")
    time.sleep(5)
