from app.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey,Float
from datetime import datetime


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    criado_em = Column(DateTime, default=datetime.now)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    total = Column(Float)

class ItemPedido(Base):
    __tablename__ = 'itens_do_pedido'
    id = Column( Integer, primary_key=True )
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    produto_id =  Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
