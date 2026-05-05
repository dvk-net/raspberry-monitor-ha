from loguru import logger
from dotenv import load_dotenv
from raspbery_monitor_ha import state_pollers
import os
import json
load_dotenv()


class Device:
    def __init__(self, device_id=None, name=None, manufacturer=None, model=None):
        self.device_id = device_id or os.getenv("DEVICE_ID")
        self.name = name or os.getenv("DEVICE_NAME")
        self.manufacturer = manufacturer or os.getenv("DEVICE_MANUFACTURER")
        self.model = model or os.getenv("DEVICE_MODEL")
        self.topic_prefix = os.getenv("TOPIC_PREFIX", "hmd")
        self.availability_topic = f"{self.topic_prefix}/device/{self.device_id}/status"

device = Device()

class Sensor:
    def __init__(self, device, name, state_topic=None, config_topic=None, unit_of_measurement=None, device_class=None, icon=None):
        self.name = name
        self.device = device
        self.state_topic = state_topic or f"{device.topic_prefix}/sensor/{device.device_id}/{name.lower()}/state"
        self.config_topic = config_topic or f"homeassistant/sensor/{device.device_id}/{name.lower()}/config"
        self.unit_of_measurement = unit_of_measurement
        self.device_class = device_class
        self.icon = icon

    def _get_config_payload(self):
        payload = {
            "name": self.name,
            "state_topic": self.state_topic,
            "unique_id": f"{self.device.device_id}_{self.name.lower()}",
            "device": {
                "identifiers": [self.device.device_id],
                "name": self.device.name,
                "manufacturer": self.device.manufacturer,
                "model": self.device.model,
            },
            "availability_topic": self.device.availability_topic,
            "payload_available": "online",
            "payload_not_available": "offline",
        }

        if self.unit_of_measurement:
            payload["unit_of_measurement"] = self.unit_of_measurement

        if self.device_class:
            payload["device_class"] = self.device_class
        
        if self.icon:
            payload["icon"] = self.icon

        return payload

    def get_state(self):
        # This method must be implemented to return the current state of the sensor
        pass

    def publish_state(self, mqtt_client):
        state = self.get_state()
        mqtt_client.publish(self.state_topic, state)
        logger.info(f"published state: {state} to {self.state_topic}")
    def publish_config(self, mqtt_client):
        config_payload = self._get_config_payload()
        mqtt_client.publish(self.config_topic, json.dumps(config_payload), retain=True)
        mqtt_client.publish(self.device.availability_topic, "online", retain=True)
        logger.info(f"published config {self.name}")
        logger.info(f"config payload: {config_payload}")


class UptimeSensor(Sensor):
    def get_state(self):
        return state_pollers.get_uptime()
    
class CPUTemperatureSensor(Sensor):
    def get_state(self):
        return state_pollers.get_cpu_temperature()
    
class WiFiDownloadSpeedSensor(Sensor):
    def get_state(self):
        return state_pollers.get_wifi_download_speed()
class WiFiUploadSpeedSensor(Sensor):
    def get_state(self):
        return state_pollers.get_wifi_upload_speed()

class CPULoadSensor(Sensor):
    def get_state(self):
        return state_pollers.get_cpu_load()
class RP1TemperatureSensor(Sensor):
    def get_state(self):
        return state_pollers.get_rp1_adc_temperature()
configured_sensors = [
    UptimeSensor(
        name="Uptime",
        device=device, 
        unit_of_measurement="s", 
        device_class="duration"
    ),
    CPUTemperatureSensor(
        name="CPU_Temperature",
        device=device,
        unit_of_measurement="°C",
        device_class="temperature"
    ),
    RP1TemperatureSensor(
        name="RP1_Temperature",
        device=device,
        unit_of_measurement="°C",
        device_class="temperature"
    ),
    WiFiDownloadSpeedSensor(
        name="WiFi_Download_Speed",
        device=device,
        unit_of_measurement="Mbit/s",
        device_class="data_rate",
        icon="mdi:download-network"
    ),
    WiFiUploadSpeedSensor(
        name="WiFi_Upload_Speed",
        device=device,
        unit_of_measurement="Mbit/s",
        device_class="data_rate",
        icon="mdi:upload-network"
    ),
    CPULoadSensor(
        name="CPU_Load",
        device=device,
        unit_of_measurement="%",
        device_class="power_factor",
        icon="mdi:cpu-64-bit"
    )
]

def on_connect(client, userdata, flags, rc):
    logger.info("Connected to MQTT broker, declaring availability")
    client.publish(device.availability_topic, "online", retain=True)
    for sensor in configured_sensors:
        sensor.publish_config(client)
