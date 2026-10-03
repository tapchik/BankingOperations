from pydantic import Field

from src.main.api.models.base_model import BaseModel


class CreditRequestRequest(BaseModel):
    accountId: int = Field(alias='account_id')
    amount: float
    termMonths: int = Field(alias='term_months')
