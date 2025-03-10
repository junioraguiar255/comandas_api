from fastapi import APIRouter, HTTPException
from domain.entities.Cliente import Cliente
from infra.orm.ClienteModel import ClienteDB
import db

router = APIRouter()

# Criar as rotas/endpoints: GET, POST, PUT, DELETE
@router.get("/cliente/", tags=["Cliente"])
async def get_cliente():
    try:
        session = db.Session()
        dados = session.query(ClienteDB).all()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/cliente/{id}", tags=["Cliente"])
async def get_cliente(id: int):
    try:
        session = db.Session()
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        return dados, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/cliente/", tags=["Cliente"])
async def post_cliente(corpo: Cliente):
    try:
        session = db.Session()

        # Verificar se o CPF já existe
        if session.query(ClienteDB).filter(ClienteDB.cpf == corpo.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

        novo_cliente = ClienteDB(None, corpo.nome, corpo.cpf, corpo.telefone)
        session.add(novo_cliente)
        session.commit()
        return {"id": novo_cliente.id_cliente}, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/cliente/{id}", tags=["Cliente"])
async def put_cliente(id: int, corpo: Cliente):
    try:
        session = db.Session()

        # Verificar se o CPF já existe (excluindo o cliente atual)
        if session.query(ClienteDB).filter(ClienteDB.cpf == corpo.cpf, ClienteDB.id_cliente != id).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

        cliente = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        cliente.nome = corpo.nome
        cliente.cpf = corpo.cpf
        cliente.telefone = corpo.telefone
        session.add(cliente)
        session.commit()
        return {"id": cliente.id_cliente}, 200
    except HTTPException as e:
        raise e
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.delete("/cliente/{id}", tags=["Cliente"])
async def delete_cliente(id: int):
    try:
        session = db.Session()
        cliente = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        session.delete(cliente)
        session.commit()
        return {"id": cliente.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()
