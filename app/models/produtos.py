from app.database import Base
from sqlalchemy import Column, Integer, String, Float



class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)
    estoque = Column(Integer)
