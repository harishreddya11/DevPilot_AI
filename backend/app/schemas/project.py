from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models.project import ProjectStatus
from pydantic import BaseModel, ConfigDict, Field



class TechStack(BaseModel):
    backend: Optional[list[str]] = None
    frontend: Optional[list[str]] = None
    database: Optional[list[str]] = None
    language: Optional[list[str]] = None
    cache: Optional[list[str]] = None
    queue: Optional[list[str]] = None
    deployment: Optional[list[str]] = None
    cloud: Optional[list[str]] = None


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    tech_stack: Optional[TechStack] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    tech_stack: Optional[TechStack] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    tech_stack: Optional[dict]
    status: str
    created_at: datetime
    updated_at: datetime