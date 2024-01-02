from typing import Any
from pydantic import BaseModel


class LoaderRequest(BaseModel):
    text: str
    privileges: int
    chat_id: str


class LoaderResponse(BaseModel):
    text: str = None
    photo: str = None
    chat_id: int or list = None
    markup: Any = None
    parse_mode: str = None
    is_extra_log: bool = True  # Нужно ли логировать название функции
