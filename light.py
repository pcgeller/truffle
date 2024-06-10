import gpiozero
from gpiozero import LED
from logging import getLogger

logger = getLogger(__name__)
class Light(LED):
    def __init__(self, pin):
        super().__init__(pin)
        logger.debug("Initializing LED with pin {}".format(pin))

    def blink(self, on_time=1, off_time=1, n=None, background=True):
        logger.debug("Blinking LED")
        if background:
            self.off()
            self.on()



