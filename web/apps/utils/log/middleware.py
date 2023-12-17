import logging
import urllib.parse
import threading

from rest_framework.response import Response

from malinka_web.malinka_web.apps.common.status_codes import StatusCodes
from malinka_web.malinka_web.apps.common.serializers import (
    RequestSerializer,
    ResponseSerializer,
)

_thread_local = threading.local()

logger = logging.getLogger('console')


def get_request():
    return getattr(_thread_local, 'current_django_request', None)


class LogRequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        self._request_info = RequestSerializer(
            url=urllib.parse.urljoin(
                f'{request.scheme}://{request.get_host()}',
                request.path
            ),
            method=f'{request.method}',
            headers=request.headers,
            cookies=request.COOKIES,
            body=request.body.decode()
        )
        response = self.get_response(request)
        resp = ResponseSerializer(
            status_code=response.status_code,
            status_text=getattr(response, 'status_text', ''),
            data=getattr(response, 'data', {}),
            headers=getattr(response, '_headers', {}),
        )

        log_request = getattr(request, 'log_request', True)

        metadata_code = None
        if isinstance(response, Response):
            metadata_code = response.data.get('metadata', {}).get('code', None)
        if (
                400 <= response.status_code < 500
        ) or (
                metadata_code is not None and
                metadata_code != StatusCodes.SUCCESS
        ):
            logger.warning(
                f'{self._request_info}. \n'
                f'Failed with: {resp}'
            )
        else:
            if log_request:
                logger.info(
                    f'{self._request_info}. \n'
                    f'Response with: {resp}'
                )
        return response

    # noinspection PyUnusedLocal
    def process_exception(self, request, exception):
        logger.error(self._request_info, exc_info=True)
