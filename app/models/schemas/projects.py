from pydantic import BaseModel
from typing import List, Optional


class ProjectInResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""


class ProjectInCreate(BaseModel):
    title: str


class ListOfProjectsInResponse(BaseModel):
    projects: List[ProjectInResponse]
    count: int
