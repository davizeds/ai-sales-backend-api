from app.database import Base, engine,SessionLocal
from app.routers import clientes,pedidos,produtos,relatorio,ia_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

db = SessionLocal()

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def rota():
    return {"message": "rota criada com sucesso"}

app.include_router(clientes.router)
app.include_router(pedidos.router)
app.include_router(produtos.router)
app.include_router(relatorio.router)
app.include_router(ia_router.router)
