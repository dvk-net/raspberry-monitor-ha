import json
from loguru import logger
from typing import Optional, Callable, Any
from raspbery_monitor_ha.devices import device

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

class Button:
    
    def __init__(self, device, name: str, icon: str = "mdi:restart", command_topic: str | None = None, config_topic: str | None = None):
        self.name = name
        self.device = device
        self.icon = icon
        self.command_topic = command_topic or f"{device.topic_prefix}/button/{device.device_id}/{name.lower()}/command"
        self.config_topic = config_topic or f"homeassistant/button/{device.device_id}/{name.lower()}/config"
    
    def _get_config_payload(self) -> dict:
        payload = {
            "name": self.name,
            "unique_id": f"{self.device.device_id}_{self.name.lower()}",
            "command_topic": self.command_topic,
            "device": {
                "identifiers": [self.device.device_id],
                "name": self.device.name,
                "manufacturer": self.device.manufacturer,
                "model": self.device.model,
            },
            "availability_topic": self.device.availability_topic,
            "payload_available": "online",
            "payload_not_available": "offline",
            "icon": self.icon,
            "entity_category": "config",  # помещает кнопку в раздел "Конфигурация"
        }
        return payload
    
    def publish_config(self, mqtt_client):
        config_payload = self._get_config_payload()
        mqtt_client.publish(self.config_topic, json.dumps(config_payload), retain=True)
        logger.info(f"Published button config: {config_payload}")
        logger.info(f"Published button topic: {self.config_topic}")
    
    def setup_callback(self, mqtt_client, callback):
        def on_message(client, userdata, msg):
            if msg.topic == self.command_topic:
                payload = msg.payload.decode()
                logger.info(f"Button {self.name} pressed, payload: {payload}")
                callback()
        
        mqtt_client.message_callback_add(self.command_topic, on_message)
        mqtt_client.subscribe(self.command_topic)
        logger.info(f"Subscribed to {self.command_topic}")

    def callback(self):
        pass

def create_sensor(
    name: str,
    get_state_func: Callable,
    device = device,
    unit_of_measurement: Optional[str] = None,
    device_class: Optional[str] = None,
    icon: Optional[str] = None,
    state_topic: Optional[str] = None,
    config_topic: Optional[str] = None
):
    """Sensor fabric"""
    
    class DynamicSensor(Sensor):
        def get_state(self):
            return get_state_func()
    
    return DynamicSensor(
        name=name,
        device=device,
        unit_of_measurement=unit_of_measurement,
        device_class=device_class,
        icon=icon,
        state_topic=state_topic,
        config_topic=config_topic
    )

def create_button(
    name: str,
    callback_func: Callable,
    device = device,
    icon: str = "mdi:restart",
    command_topic: Optional[str] = None,
    config_topic: Optional[str] = None
):

    
    class DynamicButton(Button):
        def callback(self):
            callback_func()
    
    return DynamicButton(
        name=name,
        device=device,
        icon=icon,
        command_topic=command_topic,
        config_topic=config_topic
    )