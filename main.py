from sensors import GPSSensor, WiFiSensor
import threading


def listen_for_cancel(cancel_event, *args):
    print(args)
    while not cancel_event.is_set():
        user_input = input("------Press 'q' to quit.-------")
        if user_input.lower() == 'q':
            for a in args:
                print(f'Cancelling: {a}')
                a._stop_event.set()
            cancel_event.set()
            print('Closing process')
        print('Closing user input request.')

if __name__=='__main__':
    import logging

    logging.basicConfig(
        filename='/home/pcgeller/projects/truffle/main.log',  # Name of the log file
        level=logging.DEBUG,  # Minimum log level to capture
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        filemode='w'  # Mode to open the file: 'w' for write, 'a' for append
    )
    gps_led = 22
    wifi_led = 17

    cancel_event = threading.Event()

    wifi = WiFiSensor('/home/pcgeller/projects/truffle/logs/wifi_output.txt', wifi_led, 5)
    gps = GPSSensor('/home/pcgeller/projects/truffle/logs/gps_output.txt', gps_led, 5)
    wifi.thread.start()
    gps.thread.start()
    listener_thread = threading.Thread(target=listen_for_cancel, args=(cancel_event, wifi, gps))
    listener_thread.start()


