#!/bin/bash
# Path to the log file
logfile="/var/log/wifi_networks.log"

# Ensure the log file exists
touch "$logfile"

# Scan for WiFi networks and append results to the logfile
echo "Scan on $(date)" >> "$logfile"
sudo iwlist wlan0 scan | grep 'ESSID\|Signal level' >> "$logfile"
echo "" >> "$logfile"
