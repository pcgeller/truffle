import threading
import logging

import gpiozero.exc
from gpiozero import LED
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Sensor:
    def __init__(self, output_file, pin):
        """
        A sensor represents a thread that is used to log and indicate on a data feed type.
        :parameter output_file (string): the name of the output file
        :parameter pin (int): the pin number for the LED.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_file = output_file
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run_sensor)
        self.pin = pin

    def _run(self):
        """
        Intended to be overridden by subclasses.
        :return: None
        """
        print('Running custom sensor code to start and scan.')
        pass

    def _run_sensor(self):
        """
        Used to start the sensor thread. The target function of the call to Thread.
        :return: None
        """
        self.logger.debug("Starting sensor thread.")

        while not self._stop_event.is_set():
            blinking_light = threading.Thread(target=self._blink())
            blinking_light.start()
            blinking_light.join()

        while not self._stop_event.is_set():
            self._run()


    def _setup_gpio(self):
        """
        Used to setup the GPIO LED.
        :return:
        """
        try:
            self.light = LED(self.pin)
            print(f"Setting up GPIO pin {self.pin} as output")
            print(f'Stop event is : {self._stop_event.is_set()}')
        except gpiozero.exc.BadPinFactory as pin_factory_err:
            print('Error starting pin.  Perhaps you\'re not on the remote sensor and are using a local terminal.')
            print(pin_factory_err)
            self.logger.error(pin_factory_err)

    def _blink(self):
        """
        Blink the light with timing.
        :return:
        """
        self._setup_gpio()
        while not self._stop_event.is_set():
            self.light.on()
            self.logger.debug(f"GPIO pin {self.pin} HIGH")
            sleep(0.5)
            self.light.off()
            logger.debug(f"GPIO pin {self.pin} LOW")
            sleep(0.5)

    def start(self):
        logger.debug('Starting sensor thread.')
        self.thread.start()

    def stop(self):
        logger.debug('Stopping sensor thread.')
        self._stop_event.set()
def main():
    logger.debug('Starting main loop')
    print('Starting sensor thread')
    sensor = Sensor(output_file='sensor.log', pin=0)
    sensor.start()


if __name__ == '__main__':
    main()