import logging

from apps.utils.esp8266.modules.base import Module

logger = logging.getLogger(__name__)


class Light(Module):
    def __init__(self):
        super().__init__()
        self.power: bool = False
        self.brightness: int = 64


class MainLED(Light):

    routes = {
        'power': '/main_led/{val}',
        'color': '/main_led/color?id={val}',
        'brightness': '/main_led/brightness?id={val}',
        'effect': '/main_led/effect?id={val}',
        'effect_speed': '/main_led/effect_speed?id={val}'
    }

    def __init__(self):
        super().__init__()
        self.color: int = 0
        self.effect: int = 0
        self.effect_speed: int = 20

    def power_switch(self):
        self.power = not self.power
        resource = self.get_resource(
            'power',
            params={'val': 'on' if self.power else 'off'}
        )
        self.request(resource)

    def color_switch(self, val):
        self.color = val
        resource = self.get_resource(
            'color',
            params={'val': self.color}
        )
        self.request(resource)

    def brightness_switch(self, val):
        self.brightness = val
        resource = self.get_resource(
            'brightness',
            params={'val': self.brightness}
        )
        self.request(resource)

    def effect_switch(self, val):
        self.effect = val
        resource = self.get_resource(
            'effect',
            params={'val': self.effect}
        )
        self.request(resource)

    def effect_speed_switch(self, val):
        self.effect_speed = val
        resource = self.get_resource(
            'effect_speed',
            params={'val': self.effect_speed}
        )
        self.request(resource)
