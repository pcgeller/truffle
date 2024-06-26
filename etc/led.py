from gpiozero import LED
from time import sleep
import threading

class led:
    def __init__(self, pin):
        self.pin = pin
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._blink)

    def _setup_gpio(self):
        self.light = LED(self.pin)
        print(f"Setting up GPIO pin {self.pin} as output")
        print(f'stop event is : {self._stop_event.is_set()}')

    def _blink(self):
        self._setup_gpio()
        while not self._stop_event.is_set():
            self.light.on()
            print(f"GPIO pin {self.pin} HIGH")
            sleep(0.5)
            self.light.off()
            print(f"GPIO pin {self.pin} LOW")
            sleep(0.5)

    def start_blinking(self):
        self.thread.start()

    def stop_blinking(self):
        self._stop_event.set()
        self.thread.join()

