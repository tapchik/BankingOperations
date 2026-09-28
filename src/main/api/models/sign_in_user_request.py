from src.main.api.models.base_model import BaseModel


class SignInUserRequest(BaseModel):
    username: str
    password: str
