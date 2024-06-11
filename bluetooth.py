import threading
import time
import bluetooth
import pandas as pd


# Function to discover Bluetooth devices and return their data
def discover_bluetooth_devices():
    print("Searching for Bluetooth devices...")
    devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=True)
    device_list = []

    for addr, name, device_class in devices:
        try:
            device_info = {
                "Address": addr,
                "Name": name,
                "Device Class": device_class,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            }
            device_list.append(device_info)
        except Exception as e:
            print(f"Error retrieving device info: {e}")

    return device_list


# Function to log Bluetooth data at regular intervals
def log_bluetooth_data(filename, interval):
    while True:
        devices = discover_bluetooth_devices()
        if devices:
            df = pd.DataFrame(devices)
            df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
        time.sleep(interval)


# Create a thread for logging Bluetooth data
def create_logging_thread(filename, interval):
    logging_thread = threading.Thread(target=log_bluetooth_data, args=(filename, interval))
    logging_thread.daemon = True
    logging_thread.start()


if __name__ == "__main__":
    output_file = "./output/bluetooth_log.csv"
    log_interval = 10 #seconds

    print(f"Starting Bluetooth logging thread, logging to {output_file} every {log_interval} seconds...")
    create_logging_thread(output_file, log_interval)

    # Main thread can perform other tasks or simply wait
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")
