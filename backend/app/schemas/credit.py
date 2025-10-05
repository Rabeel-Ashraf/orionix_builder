from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreditBalance(BaseModel):
    balance: int
    user_id: str

class CreditUsage(BaseModel):
    amount: int
    service: str

class CreditTransactionResponse(BaseModel):
    id: str
    amount: int
    type: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
