from app.schemas.produtos import ProdutoCreate
from app.database import SessionLocal
from app.models.produtos import Produto
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/produtos")
def criar_produto(req: ProdutoCreate):
    db = SessionLocal()
    try:
        produto = Produto(nome=req.nome,preco=req.preco,estoque=req.estoque)
        db.add( produto )
        db.commit()
        db.refresh( produto )
        return {"id": produto.id, "nome": produto.nome, "preco": produto.preco,'estoque':produto.estoque}

    finally:
        db.close()

@router.get("/produtos")
def listar_produtos():
    db = SessionLocal()
    try:
        produto = db.query(Produto).all()
        lista = []
        for arc in produto:
            lista.append({'nome': arc.nome, 'id': arc.id, 'preco': arc.preco, 'estoque': arc.estoque})
        return {'lista': lista}
    finally:
        db.close()

@router.get("/produtos/{id}")
def busca_produtos_por_id(id:int):
    db = SessionLocal()
    try:
        busca=db.query(Produto).filter(Produto.id == id).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        return {'id':busca.id,'nome':busca.nome,'preco':busca.preco,'estoque':busca.estoque}
    finally:
        db.close()

@router.put("/produtos/{id}")
def atualiza(req:ProdutoCreate,id:int):
    db = SessionLocal()
    try:
        busca = db.query( Produto ).filter(Produto.id == id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        busca.nome=req.nome
        busca.estoque=req.estoque
        busca.preco=req.preco
        db.commit()
        db.refresh( busca )
        return  {"id": busca.id,"nome": busca.nome,"preco": busca.preco,'estoque':busca.estoque}
    finally:
        db.close()


@router.delete("/produtos/{id}")
def deletar(id:int):
    db = SessionLocal()
    try:
        busca = db.query( Produto ).filter( Produto.id == id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        db.delete(busca)
        db.commit()
        return {'mensagem':'produto deletado com sucesso'}
    finally:
        db.close()
