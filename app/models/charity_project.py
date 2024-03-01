from sqlalchemy import Column, String

from app.core.db import Base, SharedFields


class CharityProject(Base, SharedFields):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)
