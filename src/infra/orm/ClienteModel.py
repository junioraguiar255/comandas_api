# Gabriel Ramos Xavier de Souza
from sqlalchemy import Column, Integer, String
import db

class ClienteDB(db.Base):
    __tablename__ = "cliente"
    
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    
    def __init__(self, id_cliente, nome, cpf, telefone):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
