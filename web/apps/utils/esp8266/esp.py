#from apps.utils.esp8266.modules.lights import MainLED
from apps.utils.esp8266.modules.lights import MainLED
from apps.utils.esp8266.modules.base import Module


class ESPScreen(Module):
    routes = {
        'brightness': '/screen/brightness?id={val}'
    }

    def __init__(self):
        super().__init__()
        self.brightness = 128

    def brightness_switch(self, val):
        self.brightness = val
        resource = self.get_resource(
            'brightness',
            params={'val': self.brightness}
        )
        self.request(resource)


class ESP:
    def __init__(self):
        self.screen = ESPScreen()
        self.main_led = MainLED()


esp = ESP()
