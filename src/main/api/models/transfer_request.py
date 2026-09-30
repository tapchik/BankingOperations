from pydantic import Field

from src.main.api.models.base_model import BaseModel


class TransferRequest(BaseModel):
    fromAccountId: int = Field(alias='from_account_id')
    toAccountId: int = Field(alias='to_account_id')
    amount: float
