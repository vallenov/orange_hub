import requests
import logging
from typing import Dict

from apps.utils.exceptions import HubException
from settings import ESP_HUB_HOST

logger = logging.getLogger(__name__)


class Module:
    ip = ESP_HUB_HOST
    routes: Dict[str, str] = {}

    def get_route(self, action):
        route = self.routes.get(action)
        if route is None:
            raise HubException(code=4, message=f'Route not found: {action}')
        return route

    def get_resource(self, action: str, params: Dict[str, str]):
        route = self.get_route(action)
        resource = route.format(**params)
        return resource

    def request(self, resource):
        resp = requests.get(f'{self.ip}{resource}')
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            logger.info(f'Get successful')
            return resp
        else:
            logger.error(f'Bad status of response: {resp.status_code}')
            raise HubException(code=1, message=f'Bad response status: {resp.status_code}')
