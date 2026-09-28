from src.main.api.models.base_model import BaseModel


class User(BaseModel):
    username: str
    role: str


class SignInUserResponse(BaseModel):
    token: str
    user: User
