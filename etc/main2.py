from etc import wifi_scanner
from etc.led import led
import threading

def listen_for_cancel(_stop_event, scanner, led):
    while not _stop_event.is_set():
        user_input = input("Press 'q' to quit: ")
        if user_input.lower() == 'q':
            scanner._stop_event.set()
            led._stop_event.set()

def run_wifi(pin):
    scanner = wifi_scanner.WifiScanner(interval=10)
    light = led(pin)
    print('start light')
    light.start_blinking()
    cancel_event = threading.Event()
    listener_thread = threading.Thread(target=listen_for_cancel, args=(cancel_event, scanner, led))
    print('***start scanner*****')
    scanner.start()
    scanner.stop()
    light.stop_blinking()

if __name__ == '__main__':
    run_wifi(17)