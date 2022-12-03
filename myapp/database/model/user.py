from database.base import Base
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
)


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, Identity(), primary_key=True)
    username = Column(String(50), index=True)
    email = Column(String(60), index=True)
    password = Column(String(120))