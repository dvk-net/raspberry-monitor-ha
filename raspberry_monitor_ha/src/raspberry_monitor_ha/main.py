import time
import paho.mqtt.client as mqtt
import os
from loguru import logger
from dotenv import load_dotenv

from raspberry_monitor_ha.client import MQTTclient
from raspberry_monitor_ha.sensors import configured_sensors
from raspberry_monitor_ha.buttons import configured_buttons
from raspberry_monitor_ha.devices import device
load_dotenv()

BROKER = os.getenv("MQTT_HOST")
DEVICE_ID = os.getenv("DEVICE_ID")
AVAIL_TOPIC = f"hmd/device/{DEVICE_ID}/status"



logger.info("=======Starting monitoring=========")
mqtt_client = MQTTclient().client

# --- LWT (если процесс умер → offline)
mqtt_client.will_set(
    AVAIL_TOPIC,
    payload="offline",
    retain=True,
)
def on_message(client, userdata, msg):
    logger.info(f"📨 RECEIVED: {msg.topic} = {msg.payload.decode()}")

def on_connect(client, userdata, flags, rc):
    logger.info("Connected to MQTT broker, declaring availability")
    client.publish(device.availability_topic, "online", retain=True)
    for sensor in configured_sensors:
        if os.getenv(f"SENSOR_{sensor.name}", "true").lower() == "false":
            sensor.delete_from_ha(client)
        else:
            sensor.publish_config(client)
    for button in configured_buttons:
        if os.getenv(f"BUTTON_{button.name}", "true").lower() == "false":
            button.delete_from_ha(client)
        else:
            button.publish_config(client)
            button.setup_callback(client, button.callback)

mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(username=os.getenv("MQTT_USERNAME"), password=os.getenv("MQTT_PASSWORD"))
mqtt_client.connect(BROKER, 1883, 60)
mqtt_client.loop_start()


while True:
    for sensor in configured_sensors:
        if os.getenv(f"SENSOR_{sensor.name}", "true").lower() == "true":
            sensor.publish_state(mqtt_client)
    time.sleep(int(os.getenv("POLLING_INTERVAL", 60)))