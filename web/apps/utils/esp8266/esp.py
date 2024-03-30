#from apps.utils.esp8266.modules.lights import MainLED
from apps.utils.esp8266.modules.lights import MainLED


class ESP:
    def __init__(self):
        self.main_led = MainLED()


esp = ESP()
