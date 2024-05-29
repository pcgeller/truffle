from sensor import Sensor
from datetime import datetime
import subprocess
import re
import csv
import gps
import time

class WiFiSensor(Sensor):
    def __init__(self, output_file, pin, interval):
        super().__init__(output_file, pin)
        self.name = 'WiFi Sensor'
        self.interval = interval

    def _run(self):
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

class GPSSensor(Sensor):
    def __init__(self, output_file, pin, interval):
        super().__init__(output_file, pin)
        self.name = 'GPS Sensor'
        self.interval = interval

    def _run(self):
        # Open a file to save the data
        with open(self.output_file, 'a') as file:
            # Start the GPS session
            session = gps.gps('localhost', '2947')
            session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

            try:
                while not self._stop_event.is_set():
                    report = session.next()
                    # Wait for a 'TPV' report and check if it has the 'lat' attribute
                    if report['class'] == 'TPV':
                        if hasattr(report, 'lat') and hasattr(report, 'lon'):
                            # Log the latitude and longitude
                            file.write(
                                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Latitude: {report.lat}, Longitude: {report.lon}\n")
                            file.flush()
                    time.sleep(10)  # Log every 10 seconds
            except KeyError:
                pass  # Ignore reports that do not contain position data
            except KeyboardInterrupt:
                exit()  # Gracefully handle Ctrl+C
