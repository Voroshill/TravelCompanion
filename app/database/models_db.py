from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    category = Column(String)

    def __repr__(self):
        return f"<Place(name={self.name}, location={self.location}, category={self.category})>"