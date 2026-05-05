# Raspberry Monitor HA

A tool to monitor Raspberry Pi metrics and integrate with Home Assistant.

## Description

This project provides a way to monitor your Raspberry Pi's system metrics such as CPU usage, temperature, memory, and disk space. It can send this data to Home Assistant for visualization and automation.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/raspbery-monitor-ha.git
   cd raspbery-monitor-ha
   ```

2. Install dependencies with Poetry:
   ```
   poetry install
   ```

3. Copy the environment example and configure your Home Assistant settings:
   ```
   cp .env-example .env
   ```
   Edit `.env` with your Home Assistant settings and API token.

4. Install as a Linux service:
   ```
   sudo cp raspbery_monitor_ha.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable raspbery_monitor_ha
   sudo systemctl start raspbery_monitor_ha
   ```

## Usage

After installation, the monitor will start collecting data and sending it to Home Assistant. Check the Home Assistant dashboard for the new sensors.