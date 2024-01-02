import os
import traceback
import datetime
import requests
import time
import urllib3
import telebot

import config
from exceptions import BotException
from loggers import get_logger
from loaders.loader import LoaderResponse

logger = get_logger(__name__)


class Bot:
    _bot = None

    @staticmethod
    def init_bot():
        Bot.bot = telebot.TeleBot(config.TOKEN)
        Bot.check_bot_connection(Bot.bot)

        @Bot.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            """
            Callback reaction
            """
            call.message.text = call.data
            Bot.log_request(call.message)
            chat_id = call.message.json['chat']['id']
            replace = Bot.replace(call.message)
            try:
                Bot.safe_send(call.message.json['chat']['id'], replace)
            except BotException:
                logger.exception(f'Message to {chat_id} is not send')
                Bot.safe_send(chat_id, LoaderResponse(text=f"Something is wrong"))

        @Bot.bot.message_handler(func=lambda message: True, content_types=config.CONTENT_TYPES)
        def send_text(message):
            """
            Text reaction
            """
            if message.content_type == 'text':
                Bot.log_request(message)
                replace = Bot.replace(message)
                chat_id = replace.chat_id
                if not chat_id:
                    chat_id = message.chat.id
                if chat_id and isinstance(chat_id, int):
                    try:
                        Bot.safe_send(chat_id, replace)
                    except BotException:
                        logger.exception(f'Message to {chat_id} is not send')
                        Bot.safe_send(message.chat.id, LoaderResponse(text=f"Something is wrong"))
                    else:
                        if chat_id != message.chat.id:
                            Bot.safe_send(message.chat.id, LoaderResponse(text=f"Something is wrong"))
                elif chat_id and isinstance(chat_id, list):
                    is_send = []
                    is_not_send = []
                    for user_chat_id in replace.chat_id:
                        try:
                            Bot.safe_send(user_chat_id, replace)
                        except BotException:
                            is_not_send.append(str(user_chat_id))
                        else:
                            is_send.append(str(user_chat_id))
                    if is_send:
                        Bot.safe_send(message.chat.id, LoaderResponse(text=f"Something is wrong"))
                    if is_not_send:
                        Bot.safe_send(message.chat.id, LoaderResponse(text=f"Something is wrong"))
            else:
                try:
                    Bot.save_file(message)
                except BotException as e:
                    logger.exception(e.context)
                    e.send_error(traceback.format_exc())
                    Bot.safe_send(message.chat.id, e.return_message())

        logger.info('Bot is started')

    @staticmethod
    def log_request(message):
        logger.info(f'Request: '
                    f'ID - {message.chat.id}, '
                    f'Login - {message.chat.username}, '
                    f'FirstName - {message.chat.first_name}')

    @staticmethod
    def init_dirs():
        """
        Init downloads dir
        """
        curdir = os.curdir
        if not os.path.exists(os.path.join(curdir, 'downloads')):
            os.mkdir(os.path.join(curdir, 'downloads'))
            os.chown(os.path.join(curdir, 'downloads'), 1000, 1000)
        if not os.path.exists(os.path.join('downloads', 'text')):
            os.mkdir(os.path.join('downloads', 'text'))
            os.chown(os.path.join('downloads', 'text'), 1000, 1000)

    @staticmethod
    def check_bot_connection(bot_obj) -> None:
        """
        Check bot connection
        """
        is_bot = None
        try:
            is_bot = bot_obj.get_me()
        except telebot.apihelper.ApiException as taa:
            logger.exception(f'{taa}')
        if not hasattr(is_bot, 'id'):
            logger.exception('Bot not found')
            send_dev_message({'subject': 'Bot not found', 'text': f'{is_bot}'})
        else:
            logger.info(f'Connection to bot success')

    @staticmethod
    def safe_send(chat_id: int, replace: LoaderResponse):
        """
        Send message with several tries
        :param chat_id: id of users chat
        :param replace: replace dict
        :return:
        """
        text = replace.text
        photo = replace.photo
        if not text and not photo:
            BotException(code=6, message='Replace is empty')
        if text:
            user = tbot_users(str(chat_id))
            text = text.replace('#%user_name%#', user.first_name or 'участник моего мини-клуба')
        is_send = False
        current_try = 0
        start = 0
        cnt_message = math.ceil(len(replace.text) / config.MESSAGE_MAX_LEN) if text else 1
        parse_mode = replace.parse_mode
        for cnt in range(cnt_message):
            while current_try < config.MAX_TRY:
                current_try += 1
                try:
                    if photo is not None:
                        if 'http' not in photo:
                            photo = open(photo, 'rb')
                        Bot._bot.send_photo(chat_id, photo=photo, caption=text)
                    elif text is not None:
                        if start + config.MESSAGE_MAX_LEN >= len(replace.text):
                            Bot._bot.send_message(
                                chat_id, text[start:],
                                reply_markup=replace.markup,
                                parse_mode=parse_mode
                            )
                        else:
                            Bot._bot.send_message(
                                chat_id,
                                text[start:start + config.MESSAGE_MAX_LEN],
                                reply_markup=replace.markup,
                                parse_mode=parse_mode
                            )
                        start += config.MESSAGE_MAX_LEN
                except ConnectionResetError as cre:
                    logger.exception(f'ConnectionResetError exception: {cre}')
                except requests.exceptions.ConnectionError as rec:
                    logger.exception(f'requests.exceptions.ConnectionError exception: {rec}')
                except urllib3.exceptions.ProtocolError as uep:
                    logger.exception(f'urllib3.exceptions.ProtocolError exception: {uep}')
                except TypeError as te:
                    logger.exception(f'File not ready yet: {te}')
                    time.sleep(1)
                except telebot.apihelper.ApiException as e:
                    logger.exception(f'Message to {chat_id} is not send')
                    raise BotException(code=1)
                except Exception as ex:
                    logger.exception(f'Unrecognized exception during a send: {traceback.format_exc()}')
                    if not is_send:
                        send_dev_message({'subject': repr(ex)[:-2], 'text': f'{traceback.format_exc()}'})
                        is_send = True
                else:
                    if text:
                        conversation_logger.info('Response: ' + text.replace('\n', ' '))
                    if photo:
                        conversation_logger.info(f'Response: {photo}')
                    logger.info(f'Number of attempts: {current_try}')
                    logger.info(f'Send successful')
                    break

    @staticmethod
    def replace(message) -> LoaderResponse:
        """
        Send result message to chat
        :param message: message from user
        :return:
        """
        start = datetime.datetime.now()
        res = {}
        chat_id = str(message.json['chat']['id'])
        if config.USE_DB:
            login = message.json['chat'].get('username', None)
            first_name = message.json['chat'].get('first_name', None)
            if chat_id not in tbot_users:
                privileges = Loader.privileges_levels['regular']
                try:
                    Bot.db_loader.add_user(chat_id=chat_id,
                                            privileges=privileges,
                                            login=login,
                                            first_name=first_name)
                except (OperationalError, exc.OperationalError) as e:
                    send_data = dict(
                        subject=f'Bot DB connection error',
                        text=f'{e}'
                    )
                    send_dev_message(data=send_data, by='telegram')
                    Bot.internet_loader.tbot_restart(privileges=privileges)
                send_data = dict(
                    subject='Bot NEW USER',
                    text=f'New user added. Chat_id: {chat_id}, login: {login}, first_name: {first_name}'
                )
                mail_resp = send_dev_message(send_data, 'mail')
                telegram_resp = send_dev_message(send_data, 'telegram')
                if mail_resp['res'] == 'ERROR' or telegram_resp['res'] == 'ERROR':
                    logger.warning(f'Message do not received. MAIL = {mail_resp}, Telegram = {telegram_resp}')
            else:
                if tbot_users(chat_id).login != login or \
                        tbot_users(chat_id).first_name != first_name:
                    DBLoader.update_user(chat_id, login, first_name)
        privileges = tbot_users(chat_id).privileges
        if message.content_type == 'text':
            form_text = message.text.strip().rstrip()
            action = form_text.split()[0].lower()
            func = Bot.mapping.get(action, Bot.file_loader.get_hello)
            request = LoaderRequest(
                text=form_text,
                privileges=privileges,
                chat_id=chat_id
            )
            log_request = None
            if config.USE_DB:
                try:
                    log_request = Bot.db_loader.log_request(
                        chat_id=chat_id
                    )
                except (OperationalError, exc.OperationalError) as e:
                    send_data = dict(subject=f'Bot DB connection error', text=f'{e}')
                    send_dev_message(data=send_data, by='telegram')
                    Bot.internet_loader.tbot_restart(request=request)
            res = asyncio.run(func(request=request)) \
                if inspect.iscoroutinefunction(func.__wrapped__) \
                else func(request=request)
            if config.USE_DB and action in Bot.mapping.keys() and res.is_extra_log:
                res.extra_log(request_id=log_request.lr_id, action=action)
        duration = datetime.datetime.now() - start
        dur = float(str(duration.seconds) + '.' + str(duration.microseconds)[:3])
        logger.info(f'Duration: {dur} sec')
        return res

    @staticmethod
    def save_file(message) -> None:
        """
        Save file
        :param message: input message
        :return:
        """
        curdir = os.curdir
        if message.content_type == 'photo':
            file_extension = '.jpg'
            file_info = Bot.bot.get_file(message.photo[-1].file_id)
        elif message.content_type == 'audio':
            file_extension = '.mp3'
            file_info = Bot.bot.get_file(message.audio.file_id)
        elif message.content_type == 'voice':
            file_extension = '.mp3'
            file_info = Bot.bot.get_file(message.voice.file_id)
        elif message.content_type == 'video':
            file_extension = '.mp4'
            file_info = Bot.bot.get_file(message.video.file_id)
        else:
            raise BotException(code=2, return_message='Я пока не умею обрабатывать этот тип данных')
        if not os.path.exists(os.path.join(curdir, 'downloads', message.content_type)):
            os.mkdir(os.path.join(curdir, 'downloads', message.content_type))
            os.chown(os.path.join(curdir, 'downloads', message.content_type), 1000, 1000)
        file_name = os.path.join(curdir, 'downloads', message.content_type,
                                 f'{now_time()}{get_hash_name()}{file_extension}')
        downloaded_info = Bot.bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_info)
        os.chown(file_name, 1000, 1000)

    @staticmethod
    def run():
        """
        Main method
        """
        Bot.init_bot()
        Bot.init_dirs()
        Bot.init_loaders()
        Bot.mapping = {
            'exchange': Bot.internet_loader.get_exchange,
            'weather': Bot.internet_loader.get_weather,
            'quote': Bot.internet_loader.get_quote,
            'wish': Bot.internet_loader.get_wish,
            'news': Bot.internet_loader.get_news,
            'affirmation': Bot.internet_loader.get_affirmation,
            'events': Bot.internet_loader.async_events,
            'food': Bot.internet_loader.get_restaurant,
            'poem': Bot.db_loader.get_poem if config.USE_DB else Bot.file_loader.get_poem,
            'divination': Bot.db_loader.poem_divination if config.USE_DB else Bot.file_loader.poem_divination,
            'movie': Bot.internet_loader.get_random_movie,
            'book': Bot.internet_loader.get_book,
            'update': Bot.db_loader.update_user_data,
            'users': Bot.db_loader.show_users,
            'hidden_functions': Bot.file_loader.get_help,
            'admins_help': Bot.file_loader.get_admins_help,
            'send_other': Bot.db_loader.send_other,
            'to_admin': Bot.db_loader.send_to_admin,
            'send_all': Bot.db_loader.send_to_all_users,
            'metaphorical_card': Bot.file_loader.get_metaphorical_card,
            'russian_painting': Bot.internet_loader.get_russian_painting,
            'ip': Bot.internet_loader.get_server_ip,
            'statistic': Bot.db_loader.get_statistic,
            'phone': Bot.internet_loader.get_phone_number_info,
            'camera': Bot.file_loader.get_camera_capture,
            'ngrok': Bot.internet_loader.ngrok,
            'serveo_ssh': Bot.internet_loader.serveo_ssh,
            'ngrok_db': Bot.internet_loader.ngrok_db,
            'restart_bot': Bot.internet_loader.tbot_restart,
            'restart_system': Bot.internet_loader.system_restart,
            'systemctl': Bot.internet_loader.systemctl,
            'allow_connection': Bot.internet_loader.allow_connection
        }
        # отправка сообщения о начале работы только с прода
        if config.PROD:
            logger.info(f'Send start message to root users')
            send_dev_message({'text': 'Bot is started'}, 'telegram')
        Bot.bot.infinity_polling(none_stop=True)
        

