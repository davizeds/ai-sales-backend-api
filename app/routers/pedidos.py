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
