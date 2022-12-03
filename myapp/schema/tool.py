from pydantic import BaseModel
from typing import List


class ToolSchema(BaseModel):
    id: int
    title: str
    link: str
    description: str
    tags: List[str]


class ToolPostSchema(BaseModel):
    title: str
    link: str
    description: str
    tags: List[str]


class TagSchema(BaseModel):
    tag: str
