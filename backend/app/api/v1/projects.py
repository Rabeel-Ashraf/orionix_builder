from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.storage_service import storage_service

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create a new project"""
    project = Project(
        **project_data.dict(),
        user_id=current_user.id
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        framework=project.framework,
        style_framework=project.style_framework,
        is_3d_enabled=project.is_3d_enabled,
        content=project.content,
        preview_url=project.preview_url,
        is_published=project.is_published,
        published_url=project.published_url,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """List all projects for current user"""
    statement = select(Project).where(Project.user_id == current_user.id)
    projects = db.exec(statement).all()
    return [ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        framework=project.framework,
        style_framework=project.style_framework,
        is_3d_enabled=project.is_3d_enabled,
        content=project.content,
        preview_url=project.preview_url,
        is_published=project.is_published,
        published_url=project.published_url,
        created_at=project.created_at,
        updated_at=project.updated_at
    ) for project in projects]

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get a specific project"""
    project = db.get(Project, project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        framework=project.framework,
        style_framework=project.style_framework,
        is_3d_enabled=project.is_3d_enabled,
        content=project.content,
        preview_url=project.preview_url,
        is_published=project.is_published,
        published_url=project.published_url,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update a project"""
    project = db.get(Project, project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update fields
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    project.updated_at = datetime.utcnow()
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        framework=project.framework,
        style_framework=project.style_framework,
        is_3d_enabled=project.is_3d_enabled,
        content=project.content,
        preview_url=project.preview_url,
        is_published=project.is_published,
        published_url=project.published_url,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete a project"""
    project = db.get(Project, project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete associated storage files
    storage_service.delete_project_files(current_user.id, project_id)
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}

@router.post("/projects/{project_id}/publish")
async def publish_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Publish a project (make it publicly accessible)"""
    project = db.get(Project, project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate public URL (this would be more sophisticated in production)
    project.is_published = True
    project.published_url = f"https://orionix.build/{current_user.username}/{project.id}"
    project.updated_at = datetime.utcnow()
    
    db.add(project)
    db.commit()
    
    return {
        "message": "Project published successfully",
        "published_url": project.published_url
    }
