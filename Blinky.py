import threading
import time
from gpiozero import LED

class GPIOLed:
    def __init__(self, pin):
        self.pin = pin
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._blink)

    def _setup_gpio(self):
        self.led = LED(self.pin)
        print(f"Setting up GPIO pin {self.pin} as output")

    def _blink(self):
        self._setup_gpio()
        while not self._stop_event.is_set():
            self.led.on()
            print(f"GPIO pin {self.pin} HIGH")
            time.sleep(0.5)
            self.led.off()
            print(f"GPIO pin {self.pin} LOW")
            time.sleep(0.5)

    def start_blinking(self):
        self.thread.start()

    def stop_blinking(self):
        self._stop_event.set()
        self.thread.join()

def scanning_process(duration):
    print("Scanning process started.")
    time.sleep(duration)  # Simulating the scanning process
    print("Scanning process finished.")

# Example usage
led = GPIOLed(pin=17)  # Assuming pin 17 for the LED
led.start_blinking()

# Start the scanning process (e.g., running for 10 seconds)
scanning_process(duration=10)

# Stop the LED blinking
led.stop_blinking()

print("LED blinking stopped.")
