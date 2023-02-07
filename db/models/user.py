from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    username: str  # Lo tipamos para que nos AYUDE a saber de que tipo es.
    email: str
