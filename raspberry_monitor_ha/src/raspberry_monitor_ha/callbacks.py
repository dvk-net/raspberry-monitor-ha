import os
import subprocess
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

def restart_service():
    logger.info("Rebooting service!")
    subprocess.run(["sudo", "systemctl", "restart", os.getenv("SERVICE_NAME", "raspberry-monitor-ha")], check=False)

def shutdown_machine():
    logger.info("Shutting down machine!")
    subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)