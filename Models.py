from DB import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

usuario_refeicao = Table( # Pra fazer uma refeição customizada, primeiro cria uma refeição, depois bota na tabela associação.
    'usuario_refeicao', Base.metadata,
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario')),
    Column('id_refeicao', Integer, ForeignKey('refeicao.id_refeicao'))
)

class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    genero = Column(String(10), nullable=False)
    altura = Column(Integer, nullable=False)
    peso = Column(Integer, nullable=False)

    refeicao = relationship(
        "Refeicao", 
        secondary=usuario_refeicao,
        back_populates="usuario"
    )

class Refeicao(Base):
    __tablename__ = 'refeicao'

    id_refeicao = Column(Integer, primary_key=True, autoincrement=True)
    nome_refeicao = Column(String(100), nullable=False)
    descricao = Column(Integer, nullable=False)

    usuario = relationship(
        "Usuario",
        secondary=usuario_refeicao,
        back_populates="refeicao"   
    )

class Alimento(Base):
    __tablename__ = 'alimento'

    id_alimento = Column(Integer, primary_key=True, autoincrement=True)
    nome_alimento = Column(String(100), nullable=False)
    unidade_padrao = Column(String(50), nullable=False)
    calorias = Column(Integer, nullable=False)
    
class Nutriente(Base):
    __tablename__ = 'nutriente'

    id_nutriente = Column(Integer, primary_key=True, autoincrement=True)
    nome_nutriente = Column(String(100), nullable=False)
    unidade_medida = Column(String(50), nullable=False)

class Registro_Diario(Base):
    __tablename__ = 'registro_diario'

    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    data = Column(String(10), nullable=False)  # Formato YYYY-MM-DDq
    log = Column(String(500), nullable=False)
