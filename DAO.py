from typing import Type, TypeVar, List, Any
from sqlalchemy.orm import Session
from DB import get_session, Base 

T = TypeVar('T', bound=Base) # Essa MERDA tá dizendo que Base é um tipo genérico, e isso não pode acontecer, MAS É MENTIRA, Base é do tipo Base, que é uma classe do SQLAlchemy, e não um tipo genérico.

class DAO:

    def __init__(self, session_factory=get_session): # Acredite se quiser, isso é um construtor
        self.session_factory = session_factory

    def adicionar_entidade(self, entidade: T) -> T:
        with self.session_factory() as session:
            session.add(entidade)
            session.commit()
            session.refresh(entidade) # Esse refresh pega os dados da entidade q tu acabou de adicionar e atualiza a variavel com eles (por isso que o return consegue retornar o ID do autoincrement)
            return entidade
        
    def obter_por_id(self, tipo_entidade: Type[T], id: int) -> T:
        with self.session_factory() as session:
            entidade_obtida = session.get(tipo_entidade, id)
            if entidade_obtida is None:
                raise ValueError(f"Entidade do tipo {tipo_entidade.__name__} com ID {id} não encontrada.")
            else:
                return entidade_obtida
            
    def atualizar_entidade(self, entidade: T) -> T:
        with self.session_factory() as session:
            entidade_atualizada = session.merge(entidade)
            session.commit()
            session.refresh(entidade_atualizada)
            return entidade_atualizada
        
    def remover_por_id(self, tipo_entidade: Type[T], id: int) -> bool:
        with self.session_factory() as session:
            entidade = session.get(tipo_entidade, id)
            if entidade:
                session.delete(entidade)
                session.commit()
                return True
            else:
                return False