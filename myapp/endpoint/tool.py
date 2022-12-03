from fastapi_utils.inferring_router import InferringRouter
from business.tool import ToolBusiness
from dependency.oauth import oauth2_scheme
from fastapi import Depends, status
from sqlalchemy.orm import Session
from database.base import get_db
from schema.tool import ToolListSchema, ToolPostSchema, ToolSchema

tool_router = InferringRouter()


@tool_router.get("/tool/all/")
async def tool_get_all(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> ToolListSchema:
    return await ToolBusiness(db).tool_get_all()


@tool_router.post("/tool/", status_code=status.HTTP_201_CREATED)
async def tool_create(
        tool_body: ToolPostSchema,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)) -> ToolSchema:
    return await ToolBusiness(db).tool_create(tool_body)
