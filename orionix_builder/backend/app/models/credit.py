from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class CreditTransaction(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    amount: int  # Positive for adding, negative for deducting
    type: str  # monthly_refill, purchase, usage_generation, etc.
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
