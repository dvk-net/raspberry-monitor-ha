import os
import psutil
import subprocess
import time
from loguru import logger
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

counter_before_down = 0
counter_before_up = 0
prev_time_up = time.time()
prev_time_down = time.time()

def get_uptime_seconds():
    with open("/proc/uptime") as f:
        total_seconds = int(float(f.readline().split()[0]))
        uptime = timedelta(seconds=total_seconds)
        
        # timedelta предоставляет дни и общие секунды
        days = uptime.days
        hours = total_seconds // 3600 % 24
        minutes = total_seconds // 60 % 60
        seconds = total_seconds % 60
        
        return f"{days}d {hours}h {minutes}m {seconds}s" if days > 0 else f"{hours}h {minutes}m {seconds}s"

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

def get_memory_available():
    return round(psutil.virtual_memory().available / (1024**3), 1)  # GB

def get_disk_usage(path="/"):
    return psutil.disk_usage(path).percent

def get_core_voltage():
    try:
        result = subprocess.run(
            ['vcgencmd', 'measure_volts', 'core'],
            capture_output=True, text=True
        )
        volt = result.stdout.split('=')[1].replace('V', '').strip()
        return float(volt)
    except:
        return None

def get_cpu_frequency():
    return round(psutil.cpu_freq().current, 0)

def get_gpu_frequency():
    try:
        result = subprocess.run(
            ['vcgencmd', 'measure_clock', 'core'],
            capture_output=True, text=True
        )
        freq = result.stdout.split('=')[1].strip()
        return round(int(freq) / 1_000_000, 0)  # MHz
    except:
        return None
    
def get_session_count_who():
    """Get the number of active sessions using the 'who' command."""
    try:
        result = subprocess.run(
            ['who'],
            capture_output=True,
            text=True,
            timeout=5
        )
        sessions = result.stdout.split('\n')[:-1]  # Exclude the trailing newline
        return len(sessions)
    except Exception as e:
        return 0