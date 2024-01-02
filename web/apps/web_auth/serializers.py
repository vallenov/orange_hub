from pydantic import BaseModel


class LoginInSerializer(BaseModel):
    login: str
    password: str
