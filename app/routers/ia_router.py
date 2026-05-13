from app.schemas.ia_schema import PerguntaIA
from fastapi import APIRouter
from app.database import SessionLocal
from app.service.relatorio_service import buscador_item_mais_vendido, busca_vendas
from app.service.ia_service import generate_response
from app.models.HistoricoIA import HistoricoIA


router = APIRouter()

@router.post('/ia/perguntar')
def perguntar(req: PerguntaIA):
    pergunta = req.pergunta.lower()
    db = SessionLocal()
    try:
        if 'produto' in pergunta and 'mais vendido' in pergunta:
            resultado = buscador_item_mais_vendido(db)
            print("RESULTADO PRODUTO MAIS VENDIDO:", resultado)
            if resultado is None:
                resposta = "Ainda não há vendas registradas para identificar o produto mais vendido."
            else:
                if isinstance(resultado, tuple):
                    mais_vendido, quantidade = resultado
                elif isinstance(resultado, dict):
                    mais_vendido = (
                        resultado.get("produto")
                        or resultado.get("produto_id")
                        or resultado.get("produto_mais_vendido")
                        or resultado.get("id")
                    )
                    quantidade = (
                        resultado.get("quantidade")
                        or resultado.get("quantidade_vendida")
                        or resultado.get("total_quantidade")
                    )
                else:
                    mais_vendido = resultado
                    quantidade = None
                if quantidade:
                    contexto = f"O produto mais vendido foi o produto de id {mais_vendido}, com {quantidade} unidades vendidas."
                else:
                    contexto = f"O produto mais vendido foi o produto de id {mais_vendido}."
                resposta = generate_response(pergunta, contexto)
            salvar_no_banco = HistoricoIA(
                pergunta=pergunta,
                resposta=resposta
            )
            db.add(salvar_no_banco)
            db.commit()
            db.refresh(salvar_no_banco)
            return {'resposta': resposta}
        elif 'total' in pergunta and ('vendido' in pergunta or 'vendi' in pergunta or 'vendas' in pergunta):
            resultado = busca_vendas(db)
            print("RESULTADO TOTAL VENDIDO:", resultado)
            if resultado is None:
                resposta = "Ainda não há vendas registradas."
            else:
                contexto = f"O total vendido no sistema foi de R$ {resultado:.2f}."
                resposta = generate_response(pergunta, contexto)
            salvar_no_banco = HistoricoIA(
                pergunta=pergunta,
                resposta=resposta
            )
            db.add(salvar_no_banco)
            db.commit()
            db.refresh(salvar_no_banco)
            return {'resposta': resposta}
        return {
            'resposta': 'Ainda não tenho resposta para essa pergunta.'
        }

    finally:
        db.close()

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
