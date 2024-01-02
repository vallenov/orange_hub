import requests

import config as config
from loggers import get_logger

logger = get_logger(__name__)


def send_dev_message(data: dict, by: str = 'mail') -> dict:
    """
    Send message to admin
    :param data: {'to': name or email, 'subject': 'subject' (unnecessary), 'text': 'text'}
    :param by: by what (mail or telegram)
    """
    resp = {}
    if by not in ('mail', 'telegram'):
        logger.error(f'Wrong parameter by ({by}) in send_dev_message')
        return dict(text=f'Wrong parameter by ({by}) in send_dev_message')
    if not data.get('to'):
        if by == 'mail':
            data.update({'to': config.MAIL.get('address')})
        else:
            data.update({'to': config.USERS.get('root_id').get('chat_id')})
    current_try = 0
    while current_try < config.MAX_TRY:
        current_try += 1
        try:
            res = requests.post(f"{config.MAIL.get('message_server_address')}{by}", data=data,
                                headers={'Connection': 'close'})
        except Exception as e:
            logger.exception(e)
        else:
            logger.info('Send successful')
            resp['res'] = res.text
            data.pop('to')
            return resp
    logger.error('Max try exceeded')
