from DB import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

class AlimentoNutriente(Base):
    __tablename__ = 'alimento_nutriente'

    id_alimento = Column(Integer, ForeignKey('alimento.id_alimento'), primary_key=True)
    id_nutriente = Column(Integer, ForeignKey('nutriente.id_nutriente'), primary_key=True)
    quantidade_por_100un = Column(Integer, nullable=False)

    alimento = relationship("Alimento", back_populates="alimento_nutrientes")
    nutriente = relationship("Nutriente", back_populates="alimento_nutrientes")

class RefeicaoAlimento(Base):
    __tablename__ = 'refeicao_alimento'

    id_refeicao = Column(Integer, ForeignKey('refeicao.id_refeicao'), primary_key=True)
    id_alimento = Column(Integer, ForeignKey('alimento.id_alimento'), primary_key=True)
    quantidade = Column(Integer, nullable=False)

    refeicao = relationship("Refeicao", back_populates="refeicao_alimento")
    alimento = relationship("Alimento", back_populates="refeicao_alimento")

class UsuarioRefeicao(Base):
    __tablename__ = 'usuario_refeicao'

    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    id_refeicao = Column(Integer, ForeignKey('refeicao.id_refeicao'), primary_key=True)

    usuario = relationship("Usuario", back_populates="usuario_refeicao")
    refeicao = relationship("Refeicao", back_populates="usuario_refeicao")

class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    genero = Column(String(10), nullable=False)
    altura = Column(Integer, nullable=False)
    peso = Column(Integer, nullable=False)

    usuario_refeicao = relationship("UsuarioRefeicao", back_populates="usuario")

class Refeicao(Base):
    __tablename__ = 'refeicao'

    id_refeicao = Column(Integer, primary_key=True, autoincrement=True)
    nome_refeicao = Column(String(100), nullable=False)
    descricao = Column(Integer, nullable=False)

    usuario_refeicao = relationship("UsuarioRefeicao", back_populates="refeicao")
    refeicao_alimento = relationship("RefeicaoAlimento", back_populates="refeicao")

class Alimento(Base):
    __tablename__ = 'alimento'

    id_alimento = Column(Integer, primary_key=True, autoincrement=True)
    nome_alimento = Column(String(100), nullable=False)
    unidade_padrao = Column(String(50), nullable=False)
    calorias = Column(Integer, nullable=False)

    id_categoria = Column(Integer, ForeignKey('categoria_alimento.id_categoria'), nullable=False)

    alimento_nutrientes = relationship("AlimentoNutriente", back_populates="alimento")
    refeicao_alimento = relationship("RefeicaoAlimento", back_populates="alimento")
    categoria = relationship("Categoria_Alimento", back_populates="alimento")
    
class Nutriente(Base):
    __tablename__ = 'nutriente'

    id_nutriente = Column(Integer, primary_key=True, autoincrement=True)
    nome_nutriente = Column(String(100), nullable=False)
    unidade_medida = Column(String(50), nullable=False)

    alimento_nutrientes = relationship("AlimentoNutriente", back_populates="nutriente")

class Registro_Diario(Base):
    __tablename__ = 'registro_diario'

    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    data = Column(String(10), nullable=False)  # Formato YYYY-MM-DDq
    log = Column(String(500), nullable=False)

class Categoria_Alimento(Base):
    __tablename__ = 'categoria_alimento'

    nome_categoria = Column(String(100), nullable=False)
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(500), nullable=True)

    alimento = relationship("Alimento", back_populates="categoria")

class Meta_Diaria(Base):
    __tablename__ = 'meta_diaria'

    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), primary_key=True)
    id_nutriente = Column(Integer, ForeignKey('nutriente.id_nutriente'), primary_key=True)
    quantidade = Column(Integer, nullable=False)
