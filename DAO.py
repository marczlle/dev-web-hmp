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
        
    def adicionar_vinculo(self, classe1, classe2, id1: int, id2: int):
        with self.session_factory() as session:
            entidade1 = session.get(classe1, id1)
            entidade2 = session.get(classe2, id2)

            if entidade1 is None or entidade2 is None:
                print(f"Uma das entidades com ID {id1} ou {id2} não foi encontrada.")
                return

            # Tenta adicionar entidade2 a algum relacionamento de entidade1
            for attr in dir(entidade1):
                try:
                    rel = getattr(entidade1, attr)
                    if isinstance(rel, list) and entidade2.__class__ in [item.class_ for item in rel.__class__.__args__]:
                        rel.append(entidade2)
                        break
                    if isinstance(rel, list) and entidade2 not in rel:
                        rel.append(entidade2)
                        break
                except Exception:
                    pass
            else:
                # Tenta o contrário
                for attr in dir(entidade2):
                    try:
                        rel = getattr(entidade2, attr)
                        if isinstance(rel, list) and entidade1 not in rel:
                            rel.append(entidade1)
                            break
                    except Exception:
                        pass
                else:
                    print("Nenhum relacionamento encontrado entre as entidades.")
                    return

            session.commit()
        
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