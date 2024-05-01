from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str


class Blog(BaseModel):
    id: int
    title: str
    body: str
    user_id: ShowUser

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: str
    password: str
