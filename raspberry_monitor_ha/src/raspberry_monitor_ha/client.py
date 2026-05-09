import json
import time
import paho.mqtt.client as mqtt
from loguru import logger
from dotenv import load_dotenv
import os
load_dotenv()

class MQTTclient:
    def __init__(self, device_id=None, broker=None, port=None, username=None, password=None):
        self.device_id = device_id or os.getenv("DEVICE_ID")
        self.broker = broker or os.getenv("MQTT_HOST")
        self.port = port or int(os.getenv("MQTT_PORT"))
        self.username = username or os.getenv("MQTT_USERNAME")
        self.password = password or os.getenv("MQTT_PASSWORD")
        self.client = mqtt.Client(client_id=self.device_id)
        self.client.username_pw_set(self.username, self.password)
        logger.info(f"MQTT client initialized with broker: {self.broker}:{self.port}")

