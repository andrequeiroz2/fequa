from pydantic import BaseModel
from typing import List


class ToolSchema(BaseModel):
    id: int
    title: str
    link: str
    description: str
    tags: List[str]


class ToolListSchema(BaseModel):
    tools: List[ToolSchema]
    total: int


class ToolPostSchema(BaseModel):
    title: str
    link: str
    description: str
    tags: List[str]

