from sensors import GPSSensor, WiFiSensor
import threading
from gpiozero import InputDevice
from signal import pause
# Define the GPIO pin connected to the toggle switch
TOGGLE_PIN = 26

# Function to execute when the toggle button is turned on
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

def toggle_switch(cancel_event, *args):
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


def execute_script():
    gps_led = 22
    wifi_led = 17
    cancel_event = threading.Event()
    wifi = WiFiSensor('/home/pcgeller/projects/truffle/output/wifi_output.csv', wifi_led, 5)
    gps = GPSSensor('/home/pcgeller/projects/truffle/output/gps_output.csv', gps_led, 5)
    wifi.thread.start()
    gps.thread.start()
    listener_thread = threading.Thread(target=listen_for_cancel, args=(cancel_event, wifi, gps))
    listener_thread.start()

if __name__=='__main__':
    import logging

    logging.basicConfig(
        filename='/home/pcgeller/projects/truffle/main.log',  # Name of the log file
        level=logging.DEBUG,  # Minimum log level to capture
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        filemode='w'  # Mode to open the file: 'w' for write, 'a' for append
    )

    toggle_switch = InputDevice(TOGGLE_PIN)
    logging.info('Starting main thread.')
    print('Main thread started.  Toggle switch to begin logging.\nListening......')
    while True:
        if toggle_switch.is_active:
            logging.info('Switch has been activated.')
            execute_script()
    pause()


