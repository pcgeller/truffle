import threading
import logging
import gpiozero.exc
from gpiozero import LED
from time import sleep

class Sensor:
    def __init__(self, output_file, pin, on_blink_timing=1, off_blink_timing=1):
        """
        A sensor represents a thread that is used to log and indicate on a data feed type.
        :parameter output_file (string): the name of the output file
        :parameter pin (int): the pin for the LED.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_file = output_file
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run_sensor)
        self.pin = pin
        self._setup_gpio()

    def run(self):
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
        self.logger.debug(f"Starting sensor run for {self.__class__.__name__}")
        runner = threading.Thread(target=self.run)
        runner.start()
        self.logger.debug("Sensor run thread complete.")



    def _setup_gpio(self):
        """
        Used to set up the GPIO LED.
        :return:
        """
        try:
            self.light = LED(self.pin)
            self.logger.info(f"Setting up GPIO pin {self.pin} as output")
        except gpiozero.exc.BadPinFactory as pin_factory_err:
            print('Error starting pin.  Perhaps you\'re not on the remote sensor and are using a local terminal.')
            print(pin_factory_err)
            self.logger.error(pin_factory_err)

    def _blink(self, on_timing=.5, off_timing=.5):
        """
        Blink the light with timing.
        :return:
        """
        if self.light is None:
            self.logger.debug('Light not initialized.  Initializing.')
            self._setup_gpio()
            self.logger.debug('Light initialized.')

        self.light.on()
        self.logger.debug(f"GPIO pin {self.pin} HIGH")
        sleep(on_timing)
        self.light.off()
        self.logger.debug(f"GPIO pin {self.pin} LOW")
        sleep(off_timing)

    def start(self):
        self.logger.info('Starting sensor thread.')
        self.thread.start()

    def stop(self):
        self.logger.info('Stopping sensor thread.')
        self._stop_event.set()

def main():
    logger = logging.getLogger(__name__)
    logger.debug('Starting main loop')
    print('Starting sensor thread')
    sensor = Sensor(output_file='sensor.log', pin=0)
    sensor.start()


if __name__ == '__main__':
    main()