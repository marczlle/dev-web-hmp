from typing import Type, TypeVar, List, Any
from sqlalchemy.orm import Session
from DB import get_session, Base 
from sqlalchemy import text

T = TypeVar('T', bound=Base)

class DAO:

    def __init__(self, session_factory=get_session): # Acredite se quiser, isso é um construtor
        self.session_factory = session_factory

    # Stored Procedures ----------------------------------------------------------------------------

    def calcular_total_nutrientes(self, id_refeicao: int): # Procedure 1
        with self.session_factory() as session:
            query = text("""
                SELECT 
                    an.id_nutriente,
                    SUM((ra.quantidade / 100.0) * an.quantidade_por_100un) AS total_nutriente
                FROM 
                    refeicao_alimento ra
                JOIN 
                    alimento_nutriente an ON ra.id_alimento = an.id_alimento
                WHERE 
                    ra.id_refeicao = :id_refeicao
                GROUP BY 
                    an.id_nutriente;
            """)

            result = session.execute(query, {'id_refeicao': id_refeicao})
            rows = result.fetchall()

            print('-=-' * 20)
            for row in rows:
                id_nutriente = row[0]
                if id_nutriente == 1:
                    id_nutriente = "Proteina"
                elif id_nutriente == 2:
                    id_nutriente = "Carboidrato"
                elif id_nutriente == 3:
                    id_nutriente = "Gordura"
                total_nutriente = row[1]
                print(f"{id_nutriente}: {total_nutriente}g")
            print('-=-' * 20)

    def buscar_por_categoria(self, categoria: str) -> List[T]:
        with self.session_factory() as session:
            query = text("SELECT id_alimento,nome_alimento,unidade_padrao,calorias FROM alimento a JOIN categoria_alimento ca ON a.id_categoria = ca.id_categoria WHERE nome_categoria = :categoria")

            result = session.execute(query, {'categoria': categoria})
            rows = result.fetchall()

            return rows
        
    def atualizar_peso_altura(self, id_usuario: int, peso_novo: int, altura_nova: int):
        with self.session_factory() as session: 

            query = text("UPDATE usuario SET peso = :peso_novo, altura = :altura_nova WHERE id_usuario = :id_usuario")

            session.execute(query, {'peso_novo': peso_novo, 'altura_nova': altura_nova, 'id_usuario': id_usuario})

            session.commit()

    def adicionar_alimento_em_refeicao(self, id_refeicao: int, id_alimento: int, quantidade: int):
        with self.session_factory() as session:
            query = text("INSERT INTO refeicao_alimento (id_refeicao, id_alimento, quantidade) VALUES (:id_refeicao, :id_alimento, :quantidade)")
            session.execute(query, {'id_refeicao': id_refeicao, 'id_alimento': id_alimento, 'quantidade': quantidade})

            session.commit()

    # CRUD Operations -----------------------------------------------------------------------------
            
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
