from app.schemas.ia_schema import PerguntaIA
from fastapi import APIRouter
from app.database import SessionLocal
from app.service.relatorio_service import buscador_item_mais_vendido



router = APIRouter()

@router.post('/ia/perguntar')
def perguntar(req:PerguntaIA):
    pergunta=req.pergunta.lower()
    if 'produto' in pergunta and 'mais vendido' in pergunta:
        db = SessionLocal()
        try:
            resultado=buscador_item_mais_vendido(db)
            if resulta == None:
                return {'resposta':'ainda nao ha vendas registradas'}
            mais_vendido,quantidade=resultado
            return {'resposta': f'o produto mais vendido foi o produto de id {mais_vendido} com uma quantidade de {quantidade} unidades vendidas'}
        finally:
            db.close()
    return {'mensagem':'ainda nao tenho resposta para essa pergunta'}
