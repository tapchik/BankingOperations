from pydantic import Field

from src.main.api.models.base_model import BaseModel


class CreditRepayResponse(BaseModel):
    # TODO: add fields with aliases
    creditId: int
    amountDeposited: float
