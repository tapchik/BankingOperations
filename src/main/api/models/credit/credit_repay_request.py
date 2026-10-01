from pydantic import Field

from src.main.api.models.base_model import BaseModel


class CreditRepayRequest(BaseModel):
    creditId: int = Field(alias='credit_id')
    accountId: int = Field(alias='account_id')
    amount: float
