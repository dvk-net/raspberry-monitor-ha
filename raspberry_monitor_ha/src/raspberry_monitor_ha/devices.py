import os
from loguru import logger
from dotenv import load_dotenv

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