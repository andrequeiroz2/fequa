from sqlalchemy.orm import Session
from database.model.tool import ToolModel
from schema.tool import ToolSchema, ToolPostSchema, TagSchema
from fastapi import HTTPException, status


class ToolBusiness:
    def __init__(self, db: Session):
        self.db = db

    async def tool_get_all(self) -> [ToolSchema]:
        """
        Lista de todas as ferramentas
        :return: lista de ToolSchema
        """
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
        return tool_list

    async def tool_get(self, tag: TagSchema) -> [ToolModel]:
        """
        Pesquisa ferramentas pela coluna tag
        :param tag: schema do pydantic
        :return: model de ferramenta
        """
        tools = self.db.query(ToolModel).filter(ToolModel.tags.any(tag.tag)).all()
        return tools

    async def tool_create(self, tool_body: ToolPostSchema) -> ToolSchema:
        """
        Cadastra uma nova ferramenta
        :param tool_body: schema do paydantic
        :return: ToolSchema
        """
        if self._get_tool_title(tool_body.title):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": "tool already registered"},
                headers={"X-Error": "UniqueViolation"}
            )

        new_tool = ToolModel(
            title=tool_body.title,
            link=tool_body.link,
            description=tool_body.description,
            tags=tool_body.tags
        )
        self.db.add(new_tool)
        self.db.commit()

        tool = self._get_tool_title(tool_body.title)

        return ToolSchema(
            id=tool.id,
            title=tool.title,
            link=tool.link,
            description=tool.description,
            tags=tool.tags
        )

    async def tool_delete(self, tool_id: int):
        """
        Deleta ferramenta, filtrando por id
        :param tool_id: id da ferramenta
        :return: Nao retorna
        """
        tool = self._get_tool_id(tool_id)
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "tool not found"},
                headers={"X-Error": "not found"}
            )
        self.db.delete(tool)

    def _get_tool_title(self, tool_title: str) -> ToolModel:
        """
        Pesquisa ferrameta por title
        :param tool_title: title da ferramenta
        :return: model de ferramenta
        """
        return self.db.query(ToolModel).filter_by(title=tool_title).first()

    def _get_tool_id(self, tool_id: int) -> ToolModel:
        """
        pesquisa ferramenta por id
        :param tool_id: id da ferramenta
        :return: model de ferramenta
        """
        return self.db.query(ToolModel).get(tool_id)
