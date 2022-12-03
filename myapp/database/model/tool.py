from database.base import Base
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
    ARRAY
)


class ToolModel(Base):
    __tablename__ = 'tools'

    id = Column(Integer, Identity(), primary_key=True)
    title = Column(String(50), index=True, unique=True)
    link = Column(String(50))
    description = Column(String(120))
    tags = Column(ARRAY(String))
