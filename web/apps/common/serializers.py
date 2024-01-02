from pydantic import BaseModel


class RequestSerializer(BaseModel):
    url: str
    method: str
    headers: dict
    cookies: dict
    body: str


class ResponseSerializer(BaseModel):
    status_code: int
    status_text: str
    data: dict
    headers: dict
