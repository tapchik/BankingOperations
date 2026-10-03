from pydantic import Field

from src.main.api.models.base_model import BaseModel


class TransferResponse(BaseModel):
    fromAccountId: int
    toAccountId: int
    fromAccountIdBalance: float
