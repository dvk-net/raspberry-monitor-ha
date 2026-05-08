# Raspberry Monitor HA

A tool to monitor Raspberry Pi metrics and integrate with Home Assistant.

## Description

This project provides a way to monitor your Raspberry Pi's system metrics such as CPU usage, temperature, memory, and disk space. It can send this data to Home Assistant for visualization and automation.

## Requirements

1. Home Assistant: it self
1. Home Assistant: Mosquitto broker (settings -> Apps -> install app -> Mosquitto broker)
1. Home Assistant: Mosquitto broker: Configuration -> add a login for authentication 
1. Raspberry Pi 5: It self
1. Raspberry Pi 5: git
1. Raspberry Pi 5: poetry

## Tested on

   - Raspberry Pi 5 (Respberry OS 64)

## Installation

1. Install poetry

1. Clone the repository:
   ```
   git clone https://github.com/dvk-net/raspberry-monitor-ha.git
   cd raspberry-monitor-ha
   ```


1. Install dependencies with Poetry:
   ```
   poetry install
   ```

3. Copy the environment example and configure your Home Assistant settings:
   ```
   cp .env-example .env
   ```
   Adjust `.env` to your Home Assistant settings and creds.

4. Install as a Linux service:

   ```
   cp cp raspberry_monitor_ha.service.example raspberry_monitor_ha.service
   # adjust raspberry_monitor_ha.service to your environment
   sudo cp raspberry_monitor_ha.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable raspberry_monitor_ha
   sudo systemctl start raspberry_monitor_ha
   ```

## Usage

After installation, the monitor will start collecting data and sending it to Home Assistant. Check the Home Assistant devices for the newly discovered device.
