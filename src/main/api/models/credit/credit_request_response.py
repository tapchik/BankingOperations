from pydantic import Field

from src.main.api.models.base_model import BaseModel


class CreditRequestResponse(BaseModel):
    # TODO: add aliases
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int
