import psutil
from loguru import logger
import time
from dotenv import load_dotenv
import os
load_dotenv()

counter_before_down = 0
counter_before_up = 0
prev_time_up = time.time()
prev_time_down = time.time()
def get_uptime():
    with open("/proc/uptime") as f:
        return int(float(f.readline().split()[0]))

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def get_cpu_temperature():
    temps = psutil.sensors_temperatures()
    if temps.get('cpu_thermal', None):
        return temps['cpu_thermal'][0].current
    elif "coretemp" in temps:
        return temps["coretemp"][0].current
    else:
        logger.info("No temp match")
        return None

def get_rp1_adc_temperature():
    temps = psutil.sensors_temperatures()
    if temps.get("rp1_adc", None):
        return temps["rp1_adc"][0].current
    else:
        return None

def get_wifi_download_speed():
    global counter_before_down, prev_time_down
    elapsed = time.time() - prev_time_down
    prev_time_down = time.time()
    net_io = psutil.net_io_counters(pernic=True)
    if counter_before_down == 0:
        counter_before_down = (net_io[os.getenv("NETWORK_INTERFACE")].bytes_recv) / (1_000_000 )
        return None
    if os.getenv("NETWORK_INTERFACE") in net_io:
        counter_now = (net_io[os.getenv("NETWORK_INTERFACE")].bytes_recv) / (1_000_000)

        speed = (counter_now - counter_before_down) / elapsed
        
        counter_before_down = counter_now
        return speed
    else:
        return None

def get_wifi_upload_speed():
    global counter_before_up, prev_time_up
    elapsed = time.time() - prev_time_up
    prev_time_up = time.time()
    net_io = psutil.net_io_counters(pernic=True)
    if counter_before_up == 0:
        counter_before_up = (net_io[os.getenv("NETWORK_INTERFACE")].bytes_sent) / (1_000_000)
        return None
    if os.getenv("NETWORK_INTERFACE") in net_io:
        counter_now = (net_io[os.getenv("NETWORK_INTERFACE")].bytes_sent ) / (1_000_000)
        speed = (counter_now - counter_before_up) / elapsed
        counter_before_up = counter_now
        return speed
    else:
        return None

def get_cpu_load():
    return psutil.cpu_percent()
