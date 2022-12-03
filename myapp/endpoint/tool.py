from fastapi_utils.inferring_router import InferringRouter
from business.tool import ToolBusiness
from dependency.oauth import oauth2_scheme
from fastapi import Depends, status
from sqlalchemy.orm import Session
from database.base import get_db
from schema.tool import ToolPostSchema, ToolSchema, TagSchema

tool_router = InferringRouter()


@tool_router.get("/")
async def root_api():
    return {
        "API": "fequa API",
        "Version": "1.0",
        "Links": ["/docs", "/redoc"]
    }


@tool_router.get("/tools")
async def tool_get_all(_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await ToolBusiness(db).tool_get_all()


@tool_router.get("/tools/")
async def tool_get(_token: str = Depends(oauth2_scheme), tag: TagSchema = Depends(), db: Session = Depends(get_db)):
    return await ToolBusiness(db).tool_get(tag)


@tool_router.post("/tools", status_code=status.HTTP_201_CREATED)
async def tool_create(
        tool_body: ToolPostSchema,
        _token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)) -> ToolSchema:
    return await ToolBusiness(db).tool_create(tool_body)


@tool_router.delete("/tools/{id}", status_code=status.HTTP_202_ACCEPTED)
async def tool_delete(
        id: int,
        _token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)):
    await ToolBusiness(db).tool_delete(id)
    return {}


