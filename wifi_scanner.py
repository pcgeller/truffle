import threading
import subprocess
import re
import time
import csv
from datetime import datetime

class WifiScanner(threading.Thread):
    def __init__(self, interval=10, output_file='wifi_scan_results.csv'):
        super().__init__()
        self.interval = interval
        self.output_file = output_file
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                output = subprocess.check_output(['iwlist', 'wlan0', 'scan'], encoding='utf-8')
                scan_results = self.parse_output(output)
                self.save_to_csv(scan_results)
            except subprocess.CalledProcessError as e:
                print(f"Failed to scan Wi-Fi networks: {e}")

            self._stop_event.wait(self.interval)

    def parse_output(self, output):
        networks = []
        cells = output.split('Cell ')
        for cell in cells[1:]:
            ssid_match = re.search(r'ESSID:"([^"]+)"', cell)
            signal_match = re.search(r'Signal level=(-\d+)', cell)
            address_match = re.search(r'Address: ([\dA-F:]+)', cell)
            if ssid_match and signal_match and address_match:
                networks.append({
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'SSID': ssid_match.group(1),
                    'Signal Level': signal_match.group(1),
                    'MAC Address': address_match.group(1)
                })
        return networks

    def save_to_csv(self, scan_results):
        file_exists = False
        try:
            with open(self.output_file, 'r') as file:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Timestamp', 'SSID', 'Signal Level', 'MAC Address'])
            if not file_exists:
                writer.writeheader()
            for network in scan_results:
                writer.writerow(network)

    def stop(self):
        self._stop_event.set()

# Example usage
scanner = WifiScanner(interval=10)
scanner.start()

# Simulate running the scanning process for a certain period
time.sleep(60)

# Stop the Wi-Fi scanner
scanner.stop()
scanner.join()

print("Wi-Fi scanning stopped.")
