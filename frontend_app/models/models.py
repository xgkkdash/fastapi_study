from sqlalchemy import Column, String

from database.database import Base


class Kvpair(Base):
    __tablename__ = "kvpairs"

    key = Column(String, primary_key=True, index=True)
    value = Column(String)
