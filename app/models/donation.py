from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.db import Base, SharedFields


class Donation(Base, SharedFields):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String)
