import time
import paho.mqtt.client as mqtt
import os
from loguru import logger
from dotenv import load_dotenv

from raspbery_monitor_ha.client import MQTTclient
from raspbery_monitor_ha.sensors import on_connect, configured_sensors
load_dotenv()

BROKER = os.getenv("MQTT_HOST")
DEVICE_ID = os.getenv("DEVICE_ID")
AVAIL_TOPIC = f"hmd/device/{DEVICE_ID}/status"




mqtt_client = MQTTclient().client

# --- LWT (если процесс умер → offline)
mqtt_client.will_set(
    AVAIL_TOPIC,
    payload="offline",
    retain=True,
)

# client.on_connect = device._on_connect
mqtt_client.on_connect = on_connect

mqtt_client.connect(BROKER, 1883, 60)
mqtt_client.username_pw_set(username=os.getenv("MQTT_USERNAME"), password=os.getenv("MQTT_PASSWORD"))
mqtt_client.loop_start()


while True:
    for sensor in configured_sensors:
        sensor.publish_state(mqtt_client)
    time.sleep(int(os.getenv("POLLING_INTERVAL", 60)))