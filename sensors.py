from sensor import Sensor
from datetime import datetime
import subprocess
import re
import csv
from gps3 import gps3
import time
import os
from time import sleep

class WiFiSensor(Sensor):
    def __init__(self, output_file, pin, interval):
        super().__init__(output_file, pin)
        self.name = 'WiFi Sensor'
        self.interval = interval

    def run(self):
        while not self._stop_event.is_set():
            self.logger.info('wifi scanning')
            print('wifi scanning')
            try:
                self._blink(.2, .2)
                output = subprocess.check_output(['iwlist', 'wlan0', 'scan'], encoding='utf-8')
                scan_results = self.parse_output(output)
                self.logger.info('Scan results: {}'.format(scan_results))
                self.save_to_csv(scan_results)
                self.logger.info('Saving results to csv file.')
            except subprocess.CalledProcessError as e:
                print(f"Failed to scan Wi-Fi networks: {e}")

            time.sleep(self.interval)

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
            self.logger.info(f'Output file is set to {self.output_file} and {os.getcwd()}')
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

    def run(self):
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()
        self.logger.info('Getting read to run GPS.')
        with open(self.output_file, mode='a', newline='') as csvfile:
            fieldnames = ['timestamp', 'latitude', 'longitude', 'altitude', 'speed', 'gps_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Log GPS data
            for new_data in gps_socket:
                self._blink(1, 1)
                if new_data:
                    data_stream.unpack(new_data)
                    latitude = data_stream.TPV['lat']
                    longitude = data_stream.TPV['lon']
                    altitude = data_stream.TPV['alt']
                    speed = data_stream.TPV['speed']
                    gps_time = data_stream.TPV['time']
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                    print('Logging GPS Data')
                    writer.writerow({'timestamp': timestamp,
                                     'latitude': latitude,
                                     'longitude': longitude,
                                     'altitude': altitude,
                                     'speed': speed,
                                     'gps_time': gps_time})
                    csvfile.flush()
                    self.logger.info(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}, Speed: {speed}")
                    time.sleep(self.interval)
                if self._stop_event.is_set():
                    self.logger.info('Stopping gps sensor')
                    csvfile.close()
                    self.logger.info(f'CSV File is closed. :{csvfile.closed}')
 #                   gps_socket.close()
  #                  self.logger.info(f'GPSD Socket is closed.')
                    break


class BluetoothSensor(Sensor):
    def __init__(self, output_file, pin, interval):
        super().__init__(output_file, pin)
        self.name = 'Bluetooth Sensor'
        self.interval = interval
        self.logger.info('Bluetooth sensor initialized.')

    def run(self):

        pass
