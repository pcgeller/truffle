import subprocess
from time import sleep
from gps_logger import log_gps_data
from gpiozero import LED
import threading

gps_led = LED(22)
wifi_led = LED(17)

def log_wifi(script_path):
    wifi_led.on()
    sleep(1)
    wifi_led.off()

    subprocess.Popen('sh', script_path, '&')

def log_gps():
    gps_led.on()
    sleep(1)
    gps_led.off()
    t = threading.Thread(target=log_gps_data,
                         name='logging_gps')  # < Note that I did not actually call the function, but instead sent it as a parameter
    t.daemon=True
    t.start()

if __name__=='__main__':
    log_wifi('./wifi_logger.sh')
    log_gps()
    all_led = LED(27)
    all_led.on()
