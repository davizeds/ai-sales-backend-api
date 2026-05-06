from app.models.pedido import Pedido, ItemPedido

def busca_vendas(db):
    busca = db.query(Pedido).all()
    total_vendido=0
    for pedidos in busca:
        total_vendido += pedidos.total
    return total_vendido



def buscador_item_mais_vendido(db):
    vendas_por_produto= {}
    if not vendas_por_produto:
        return None
    busca = db.query( ItemPedido ).all()
    for p in busca:
        vendas_por_produto[p.produto_id] =  vendas_por_produto.get(p.produto_id, 0) + p.quantidade
    mais_vendido = max( vendas_por_produto, key= vendas_por_produto.get) if  vendas_por_produto else None
    quantidade = vendas_por_produto[mais_vendido]
    return mais_vendido,quantidade
