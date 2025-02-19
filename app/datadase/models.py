from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from .database import Base


class Client(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)

class ClientAuth(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, nullable=False)
