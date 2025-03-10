# Gabriel Ramos Xavier de Souza
from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

# Import das classes com as rotas/endpoints
from app import FuncionarioDAO
from app import ClienteDAO
from app import ProdutoDAO  # Importando o ProdutoDAO

app = FastAPI()

# Mapeamento das rotas/endpoints
app.include_router(FuncionarioDAO.router)
app.include_router(ClienteDAO.router)
app.include_router(ProdutoDAO.router)  # Incluindo o ProdutoDAO

@app.get("/")
def root():
    return {"detail": "API Pastelaria: http://127.0.0.1:8000/docs#/"}

if __name__ == "__main__":
    uvicorn.run('main:app', host=HOST, port=int(PORT), reload=RELOAD)
