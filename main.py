from sensors import GPSSensor, WiFiSensor
import threading

def listen_for_cancel(_stop_event, *args):
    while not _stop_event.is_set():
        user_input = input("Press 'q' to quit: ")
        if user_input.lower() == 'q':
            for a in args:
                print(f'Cancelling: {a}')
                a._stop_event.set()

if __name__=='__main__':
    import logging

    logging.basicConfig(
        filename='main.log',  # Name of the log file
        level=logging.DEBUG,  # Minimum log level to capture
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        filemode='w'  # Mode to open the file: 'w' for write, 'a' for append
    )
    gps_led = 22
    wifi_led = 17

    cancel_event = threading.Event()

    wifi = WiFiSensor(f'./logs/wifi_output.txt', wifi_led, 10)
    gps = GPSSensor(f'./logs/gps_output.txt', gps_led, 10)
    wifi.start()
    gps.start()
    listener_thread = threading.Thread(target=listen_for_cancel, args=(cancel_event, wifi))


