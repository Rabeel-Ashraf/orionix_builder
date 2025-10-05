from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    framework: str = "react"
    style_framework: str = "tailwind"
    is_3d_enabled: bool = False

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None

class ProjectResponse(ProjectBase):
    id: str
    user_id: str
    content: Optional[Dict[str, Any]] = None
    preview_url: Optional[str] = None
    is_published: bool
    published_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
