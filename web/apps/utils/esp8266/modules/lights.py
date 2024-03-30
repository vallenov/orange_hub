import requests
import logging

from apps.utils.exceptions import HubException

logger = logging.getLogger(__name__)


class Light:
    def __init__(self):
        self.power: bool = False
        self.brightness: int = 64


class MainLED(Light):
    ip = 'http://192.168.0.100'

    class Routes:
        power = '/main_led/{val}'
        color = '/main_led/color?id={val}'
        brightness = '/main_led/brightness?id={val}'
        effect = '/main_led/effect?id={val}'
        effect_speed = '/main_led/effect_speed?id={val}'

    def __init__(self):
        super().__init__()
        self.color: int = 0
        self.effect: int = 0
        self.effect_speed: int = 20

    def request(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            logger.info(f'Get successful')
            return resp
        else:
            logger.error(f'Bad status of response: {resp.status_code}')
            raise HubException(code=1, message=f'Bad response status: {resp.status_code}')

    def power_switch(self):
        self.power = not self.power
        params = {'val': 'on' if self.power else 'off'}
        url = f'{self.ip}{self.Routes.power.format(**params)}'
        self.request(url)

    def color_switch(self, val):
        self.color = val
        params = {'val': self.color}
        url = f'{self.ip}{self.Routes.color.format(**params)}'
        self.request(url)

    def brightness_switch(self, val):
        self.brightness = val
        params = {'val': self.brightness}
        url = f'{self.ip}{self.Routes.brightness.format(**params)}'
        self.request(url)

    def effect_switch(self, val):
        self.effect = val
        params = {'val': self.effect}
        url = f'{self.ip}{self.Routes.effect.format(**params)}'
        self.request(url)

    def effect_speed_switch(self, val):
        self.effect_speed = val
        params = {'val': self.effect_speed}
        url = f'{self.ip}{self.Routes.effect_speed.format(**params)}'
        self.request(url)
