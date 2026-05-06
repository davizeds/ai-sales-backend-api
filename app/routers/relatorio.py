from app.database import SessionLocal
from fastapi import APIRouter
from app.models.pedido import Pedido, ItemPedido

router = APIRouter()


@router.get("/total_vendido")
def busca_vendas():
    db = SessionLocal()
    try:
        busca = db.query(Pedido).all()
        total_vendido=0
        for pedidos in busca:
            total_vendido += pedidos.total
        return {'total_vendido': total_vendido}
    finally:
        db.close()


@router.get("/produto_mais_vendido")
def buscador_item_mais_vendido():
    db = SessionLocal()
    vendas_por_produto= {}
    try:
        busca = db.query( ItemPedido ).all()
        for p in busca:
            vendas_por_produto[p.produto_id] =  vendas_por_produto.get(p.produto_id, 0) + p.quantidade
        mais_vendido = max( vendas_por_produto, key= vendas_por_produto.get) if  vendas_por_produto else None
        return {'mais_vendido':mais_vendido}
    finally:
        db.close()
