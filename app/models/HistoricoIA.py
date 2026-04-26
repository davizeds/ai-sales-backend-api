from app.database import Base
from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime

class HistoricoIA(Base):
    __tablename__ = 'historico_ia'

    id = Column( Integer, primary_key=True )
    pergunta = Column( String )
    resposta = Column( String )
    criado_em = Column( DateTime, default=datetime.now )
