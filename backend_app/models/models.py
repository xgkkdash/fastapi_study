from sqlalchemy import Column, String, Integer

from database.database import Base


class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
