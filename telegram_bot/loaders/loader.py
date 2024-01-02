from pydantic import BaseModel
from telebot.types import InlineKeyboardMarkup


class LoaderRequest(BaseModel):
    text: str
    privileges: int
    chat_id: str


class LoaderResponse(BaseModel):
    text: str = None
    photo: str = None
    chat_id: int or list = None
    markup: InlineKeyboardMarkup = None
    parse_mode: str = None
    is_extra_log: bool = True  # Нужно ли логировать название функции
