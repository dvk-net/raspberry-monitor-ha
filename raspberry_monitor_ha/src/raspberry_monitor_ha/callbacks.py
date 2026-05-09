import subprocess
from loguru import logger

def restart_service():
    logger.info("Rebooting service!")
    subprocess.run(["sudo", "systemctl", "restart", "raspberry-monitor-ha"], check=False)