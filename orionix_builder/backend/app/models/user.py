from sqlmodel import SQLModel, Field, Column, String
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    username: str = Field(index=True)
    hashed_password: Optional[str] = None
    plan: str = Field(default="free")  # free, basic, pro, enterprise
    credits: int = Field(default=50)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # OAuth fields
    google_id: Optional[str] = Field(default=None, index=True)
    avatar: Optional[str] = None
