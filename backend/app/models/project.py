from sqlmodel import SQLModel, Field, Column, String, JSON
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class Project(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    name: str = Field(index=True)
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    preview_url: Optional[str] = None
    is_published: bool = Field(default=False)
    published_url: Optional[str] = None
    storage_path: Optional[str] = None  # Path in S3/MinIO
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Project settings
    framework: str = Field(default="react")  # react, vue, html, etc.
    style_framework: str = Field(default="tailwind")  # tailwind, bootstrap, etc.
    is_3d_enabled: bool = Field(default=False)
