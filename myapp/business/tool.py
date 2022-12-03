from sqlalchemy.orm import Session

from database.model.tool import ToolModel
from schema.tool import ToolSchema, ToolListSchema, ToolPostSchema


class ToolBusiness:
    def __init__(self, db: Session):
        self.db = db

    async def tool_get_all(self):
        tool_list = []
        for tool in self.db.query(ToolModel).all():
            tool_list.append(
                ToolSchema(
                    id=tool.id,
                    title=tool.title,
                    link=tool.link,
                    description=tool.description,
                    tags=tool.tags
                )
            )
        return ToolListSchema(tools=tool_list, total=self.db.query(ToolModel).count())

    async def tool_create(self, tool_body: ToolPostSchema) -> ToolSchema:

        new_tool = ToolModel(
            title=tool_body.title,
            link=tool_body.link,
            description=tool_body.description,
            tags=tool_body.tags
        )
        self.db.add(new_tool)
        self.db.commit()

        tool = self._get_tool(tool_body.title)

        return ToolSchema(
            id=tool.id,
            title=tool.title,
            link=tool.link,
            description=tool.description,
            tags=tool.tags
        )

    def _get_tool(self, tool_title: str):
        return self.db.query(ToolModel).filter_by(title=tool_title).first()
