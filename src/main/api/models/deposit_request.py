from pydantic import Field

from src.main.api.models.base_model import BaseModel


class DepositRequest(BaseModel):
    accountId: int = Field(alias='account_id')
    amount: float
