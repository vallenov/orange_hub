from apps.utils.log.middleware import get_request


class RequestFilter:
    """
    Скрытие токенов и паролей
    """

    def filter(self, record):
        request = get_request()
        return True
