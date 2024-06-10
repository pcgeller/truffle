from gpiozero import Button
from threading import Thread
import time

# Define GPIO pin
button_pin = 26

# Set up the button
button = Button(button_pin, pull_up=True)

def button_listener():
    while True:
        if button.is_pressed:
            print("Button Pressed")
            # Add your action here
            time.sleep(0.2)  # Debounce delay

def main():
    # Start the button listener thread
    button_thread = Thread(target=button_listener)
    button_thread.daemon = True
    button_thread.start()

    try:
        while True:
            # Main program loop
            # Add other tasks here
            print('waiting')
            time.sleep(1)  # Simulating other tasks

    except KeyboardInterrupt:
        print("Program terminated")

if __name__ == "__main__":
    main()
