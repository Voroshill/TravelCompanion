from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Place(Base):
    __tablename__ = 'place'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    location: str = Column(String)
    category: str = Column(String)

    def __repr__(self) -> str:
        return f"<Place(name={self.name}, location={self.location}, category={self.category})>"
