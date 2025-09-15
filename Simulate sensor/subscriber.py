import os
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions
from dotenv import load_dotenv

load_dotenv()

# InfluxDB config
url = os.getenv("INFLUX_URL")
token = os.getenv("INFLUX_TOKEN") 
org = os.getenv("INFLUX_ORG")
bucket = os.getenv("INFLUX_BUCKET")


client_influx = InfluxDBClient(url=url, token=token, org=org)
write_api = client_influx.write_api(write_options=WriteOptions(batch_size=1))

# MQTT config
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "sensors/data"

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temperature = data.get("temperature")
        humidity = data.get("humidity")

        point = (
            Point("sensor_data")
            .tag("device", "sensor-01")
            .field("temperature", temperature)
            .field("humidity", humidity)
        )

        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Saved -> Temperature: {temperature}, Humidity: {humidity}")

    except Exception as e:
        print("Error:", e)

client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message
client_mqtt.connect(BROKER, PORT, 60)
client_mqtt.subscribe(TOPIC)

print("Listening for data...")
client_mqtt.loop_forever()
