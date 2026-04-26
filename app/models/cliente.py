from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    criado_em = Column(DateTime, default=datetime.now)
