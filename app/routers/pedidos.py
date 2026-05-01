from app.schemas.pedidos import PedidoCreate
from app.database import SessionLocal
from app.models.pedido import  Pedido,ItemPedido
from fastapi import APIRouter, HTTPException
from app.models.cliente import Cliente
from app.models.produtos import Produto

router = APIRouter()

@router.post("/pedidos")
def pedido(req: PedidoCreate):
    db = SessionLocal()
    total = 0
    try:
        busca = db.query( Cliente ).filter( Cliente.id == req.cliente_id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        criar_pedido = Pedido( cliente_id=req.cliente_id,total=0)
        db.add( criar_pedido )
        db.commit()
        db.refresh( criar_pedido )
        for item in req.itens:
            produto = db.query( Produto ).filter( Produto.id ==  item.produto_id ).first()
            if not produto:
                raise HTTPException( status_code=404, detail='esse id nao existe' )
            if  produto.estoque  <   item.quantidade:
                raise HTTPException( status_code=404, detail='produto insuficiente' )
            subtotal = (produto.preco * item.quantidade)
            total += subtotal
            produto.estoque -= item.quantidade
            criar_item_pedido = ItemPedido(quantidade=item.quantidade, produto_id=produto.id, pedido_id=criar_pedido.id,preco_unitario=produto.preco)
            db.add(  criar_item_pedido )
        criar_pedido.total = total
        db.commit()
        db.refresh(criar_pedido)
        return {'id_do_pedido':criar_pedido.id,'cliente_id':req.cliente_id,'total':total,'mensagem':'sucesso'}
    finally:
        db.close()

@router.get('/pedidos')
def listar_pedidos():
    db = SessionLocal()
    try:
        pedidos = db.query(Pedido).all()
        resultado = []
        for p in pedidos:
            itens = db.query(ItemPedido).filter(ItemPedido.pedido_id == p.id).all()
            lista_itens = [
                {'produto_id': item.produto_id, 'quantidade': item.quantidade, 'preco_unitario': item.preco_unitario}
                for item in itens
]
            resultado.append({'id': p.id, 'cliente_id': p.cliente_id, 'total': p.total, 'itens': lista_itens})
        return {'resultado':resultado}
    finally:
        db.close()

@router.get('/pedidos/{id}')
def busca_pedido_por_id(id:int):
    db = SessionLocal()
    try:
        busca = db.query( Pedido ).filter(  Pedido.id == id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        itens=db.query(ItemPedido).filter(ItemPedido.pedido_id==busca.id).all()
        lista_itens=[]
        for i in itens:
            lista_itens.append(
             {'produto_id': i.produto_id, 'quantidade': i.quantidade, 'preco_unitario': i.preco_unitario})
        return {'id': busca.id, 'cliente_id': busca.cliente_id, 'total': busca.total, 'itens': lista_itens}
    finally:
        db.close()

@router.delete("/pedidos/{id}")
def deletar(id:int):
    db = SessionLocal()
    try:
        busca = db.query( Pedido ).filter( Pedido.id == id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        itens = db.query( ItemPedido ).filter( ItemPedido.pedido_id == busca.id ).all()
        for i in itens:
            produto=db.query( Produto ).filter(Produto.id== i.produto_id ).first()
            if produto:
                produto.estoque += i.quantidade
            db.delete(i)
        db.delete(busca)
        db.commit()
        return {'mensagem':'pedido deletado com sucesso'}
    finally:
        db.close()
