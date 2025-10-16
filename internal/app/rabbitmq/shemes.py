from pydantic import BaseModel


class Response(BaseModel):
    msg: str = ''
    success: bool
    data: list[dict] = []
    err: str = ''