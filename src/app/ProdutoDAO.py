# Gabriel Ramos Xavier de Souza
import db
from fastapi import APIRouter
from infra.orm.ProdutoModel import ProdutoDB
from domain.entities.Produto import Produto

router = APIRouter()

# Buscar todos os produtos
@router.get("/produto/", tags=["Produto"])
async def get_produto():
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Buscar um produto pelo ID
@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int):
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one_or_none()
        if dados:
            return dados, 200
        return {"erro": "Produto não encontrado"}, 404
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Criar um novo produto
@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto):
    try:
        session = db.Session()
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, corpo.foto, corpo.valor_unitario)
        session.add(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Atualizar um produto existente
@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one_or_none()
        if not dados:
            return {"erro": "Produto não encontrado"}, 404
        
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        dados.foto = corpo.foto
        dados.valor_unitario = corpo.valor_unitario

        session.add(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Deletar um produto pelo ID
@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int):
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one_or_none()
        if not dados:
            return {"erro": "Produto não encontrado"}, 404

        session.delete(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()
