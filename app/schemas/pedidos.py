from pydantic import BaseModel
from typing import List

class ItemPedidoCreate(BaseModel):
    quantidade: int
    produto_id: int

class PedidoCreate(BaseModel):
    cliente_id: int
    itens:List[ItemPedidoCreate]
