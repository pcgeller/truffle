import wifi_scanner
from led import led
from time import sleep

def run_wifi(pin):
    scanner = wifi_scanner.WifiScanner(interval=10)
    light = led(pin)
    print('start light')
    light.start_blinking()
    print('***start scanner*****')
    scanner.start()
    sleep(15)
    scanner.stop()
    light.stop_blinking()

if __name__ == '__main__':
    run_wifi(17)