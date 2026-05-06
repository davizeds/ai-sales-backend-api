from app.schemas.ia_schema import PerguntaIA
from fastapi import APIRouter
from app.database import SessionLocal
from app.service.relatorio_service import buscador_item_mais_vendido, busca_vendas
from app.service.ia_service import generate_response
from app.models.HistoricoIA import HistoricoIA


router = APIRouter()

@router.post('/ia/perguntar')
def perguntar(req:PerguntaIA):
    pergunta=req.pergunta.lower()
    if 'produto' in pergunta and 'mais vendido' in pergunta:
        db = SessionLocal()
        try:
            resultado=buscador_item_mais_vendido(db)
            if resultado == None:
                return {'resposta':'ainda nao ha vendas registradas'}
            mais_vendido,quantidade=resultado
            contexto=f'o produto mais vendido foi o produto de id {mais_vendido} com uma quantidade de {quantidade} unidades vendidas'
            resposta = generate_response( pergunta, contexto )
            salavar_no_banco=HistoricoIA(pergunta=pergunta,resposta=resposta)
            db.add(  salavar_no_banco )
            db.commit()
            db.refresh( salavar_no_banco )
            return {'resposta': resposta}
        finally:
            db.close()

    elif 'total' in pergunta and 'vendido' in pergunta:
        db = SessionLocal()
        try:
            resultado = busca_vendas(db)
            if resultado == None:
                return {'resposta': 'ainda nao ha vendas registradas'}
            total_vendido=resultado
            contexto = f'o total vendido foi de {total_vendido}'
            resposta = generate_response( pergunta, contexto )
            salavar_no_banco = HistoricoIA( pergunta=pergunta, resposta=resposta )
            db.add(  salavar_no_banco )
            db.commit()
            db.refresh(  salavar_no_banco )
            return {'resposta': resposta}
        finally:
            db.close()
    return {'mensagem':'ainda nao tenho resposta para essa pergunta'}

@router.get('/ia/historico')
def pegar_historico():
    db = SessionLocal()
    historico=[]
    try:
        lista=db.query(HistoricoIA).all()
        for h in lista:
            historico.append({'id':h.id,'pergunta':h.pergunta,'resposta':h.resposta})
        return {'historico':historico}
    finally:
        db.close()
