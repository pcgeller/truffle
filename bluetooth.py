import threading
import subprocess
import os
import datetime


def log_bluetooth_signals(output_file):
    cmd = ['sudo', 'hcitool', 'lescan', '--duplicates']
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as lescan_proc:
        try:
            cmd = ['sudo', 'hcidump', '--raw']
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as hcidump_proc:
                with open(output_file, 'w') as f:
                    while True:
                        line = hcidump_proc.stdout.readline()
                        if not line:
                            break
                        timestamp = datetime.datetime.now().isoformat()
                        f.write(f"{timestamp}: {line.decode('utf-8')}")
        except KeyboardInterrupt:
            lescan_proc.terminate()
            hcidump_proc.terminate()


def start_logging(output_file):
    log_thread = threading.Thread(target=log_bluetooth_signals, args=(output_file,))
    log_thread.daemon = True
    log_thread.start()
    return log_thread


def main():
    output_file = '/path/to/bluetooth_log.txt'

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    print(f"Starting Bluetooth logging, output file: {output_file}")
    log_thread = start_logging(output_file)

    try:
        while True:
            # Main program loop (perform other tasks here)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated")


if __name__ == "__main__":
    main()
