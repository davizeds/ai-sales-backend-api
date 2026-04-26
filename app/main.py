from app.database import Base, engine,SessionLocal
from app.models.produtos import Produto

db = SessionLocal()

Base.metadata.create_all(engine)
