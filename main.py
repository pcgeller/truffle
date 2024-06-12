from sensors import GPSSensor, WiFiSensor
import threading
from gpiozero import Button
from gpiozero import LED
from signal import pause
# Define the GPIO pin connected to the toggle switch
import time


# Function to execute when the toggle button is turned on
def listen_for_cancel(cancel_event, *args):
    print(args)
    while not cancel_event.is_set():
        print('Untoggle switch to close down process.')
        if toggle_switch.is_active == False:
            for arg in args:
                print(f'Cancelling: {arg}')
                arg._stop_event.set()
                cancel_event.set()
                print(f'Closing process {arg}')
            print('All processes are cancelled.')
            time.sleep(10)

def execute_script():
    gps_led = 22 #1st light - green
    wifi_led = 17 #2nd light - green
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
        filename='/home/pcgeller/projects/truffle/logs/main.log',  # Name of the log file
        level=logging.DEBUG,  # Minimum log level to capture
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
        filemode='w'  # Mode to open the file: 'w' for write, 'a' for append
    )

    status_light = LED(27) #3rd light - red
    status_light.blink(on_time=.25, off_time=1, background=True)
    TOGGLE_PIN = 26
    toggle_switch = Button(TOGGLE_PIN)
    logging.info('Starting main thread.')
    print('Main thread started.  Toggle switch to begin logging.\nListening......')
    while True:
        if toggle_switch.is_active:
            logging.info('Switch has been activated.')
            execute_script()
    pause()
    print('end of program')


