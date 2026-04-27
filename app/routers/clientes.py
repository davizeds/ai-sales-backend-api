from app.schemas.cliente_schema import ClienteCreate,ClienteUpdate
from fastapi import APIRouter
from app.database import SessionLocal
from app.models.cliente import Cliente



router = APIRouter()

@router.post("/clientes")
def criacao_cliente(req:ClienteCreate):
    db = SessionLocal()
    try:
        cliente = Cliente(nome=req.nome, email= req.email)
        db.add( cliente )
        db.commit()
        db.refresh( cliente )
        return {"id": cliente.id,"nome": cliente.nome,"email": cliente.email}
    finally:
        db.close()

@router.get("/cliente")
def buscador():
    db = SessionLocal()
    try:
        clientes = db.query(Cliente).all()
        lista = []
        for arc in clientes:
            lista.append({'nome': arc.nome, 'id': arc.id, 'email': arc.email, 'criado_em': arc.criado_em})
        return {'lista': lista}
    finally:
        db.close()


@router.get("/clientes/{id}")
def busca_id(id:int):
    db = SessionLocal()
    try:
        busca=db.query(Cliente).filter(Cliente.id == id).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        return {'id':busca.id,'nome':busca.nome,'email':busca.email,'criado_em':busca.criado_em}
    finally:
        db.close()

@router.put("/clientes/{id}")
def atualiza(req:ClienteUpdate,id:int):
    db = SessionLocal()
    try:
        busca = db.query( Cliente ).filter( Cliente.id == id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        busca.nome=req.nome
        busca.email=req.email
        db.commit()
        db.refresh( busca )
        return  {"id": busca.id,"nome": busca.nome,"email": busca.email}
    finally:
        db.close()


@router.delete("/clientes/{id}")
def deletar(id:int):
    db = SessionLocal()
    try:
        busca = db.query( Cliente ).filter( Cliente.id == id ).first()
        if not busca:
            raise HTTPException( status_code=404, detail='esse id nao existe' )
        db.delete(busca)
        db.commit()
        return {'mensagem':'cliente deletado com sucesso'}
    finally:
        db.close()
