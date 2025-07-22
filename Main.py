from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB import Base
from Models import Alimento, Nutriente, AlimentoNutriente, Categoria_Alimento

# Conectar ao banco
engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Categoria genérica
# Adicionando uma verificação para não duplicar
if not session.query(Categoria_Alimento).first():
    categoria = Categoria_Alimento(nome_categoria="Comida", descricao="Alimentos diversos")
    session.add(categoria)
    session.commit()
categoria = session.query(Categoria_Alimento).first()


# Nutrientes
# Adicionando uma verificação para não duplicar
if not session.query(Nutriente).first():
    nutrientes_data = {
        "Gordura": Nutriente(nome_nutriente="Gordura", unidade_medida="g"),
        "Fibra": Nutriente(nome_nutriente="Fibra", unidade_medida="g"),
        "Proteína": Nutriente(nome_nutriente="Proteína", unidade_medida="g"),
        "Carboidrato": Nutriente(nome_nutriente="Carboidrato", unidade_medida="g"),
    }
    session.add_all(nutrientes_data.values())
    session.commit()
nutrientes = {n.nome_nutriente: n for n in session.query(Nutriente).all()}


# Alimentos
alimentos_data = [
    ("Frango Grelhado", 165, "100g", {"Proteína": 31.0, "Gordura": 3.6, "Carboidrato": 0.0, "Fibra": 0.0}),
    ("Arroz Integral", 124, "1 xícara (100g)", {"Proteína": 2.6, "Gordura": 1.0, "Carboidrato": 25.8, "Fibra": 1.6}),
    ("Feijão Preto Cozido", 132, "1 concha (130g)", {"Proteína": 8.9, "Gordura": 0.8, "Carboidrato": 23.7, "Fibra": 8.7}),
    ("Maçã", 52, "1 un (130g)", {"Proteína": 0.3, "Gordura": 0.2, "Carboidrato": 13.8, "Fibra": 2.4}),
    ("Ovo Cozido", 78, "1 un (50g)", {"Proteína": 6.3, "Gordura": 5.3, "Carboidrato": 0.6, "Fibra": 0.0}),
    ("Pão Integral", 69, "1 fatia (30g)", {"Proteína": 3.6, "Gordura": 1.1, "Carboidrato": 11.6, "Fibra": 1.9}),
    ("Iogurte Natural Integral", 61, "1 copo (100ml)", {"Proteína": 3.5, "Gordura": 3.3, "Carboidrato": 4.7, "Fibra": 0.0}),
    ("Salmão Grelhado", 208, "100g", {"Proteína": 20.0, "Gordura": 13.0, "Carboidrato": 0.0, "Fibra": 0.0}),
    ("Banana Prata", 89, "1 un (100g)", {"Proteína": 1.1, "Gordura": 0.3, "Carboidrato": 22.8, "Fibra": 2.6}),
    ("Pizza de Pepperoni", 285, "1 fatia (107g)", {"Proteína": 11.0, "Gordura": 12.0, "Carboidrato": 33.0, "Fibra": 2.0}),
]

# Inserir alimentos e nutrientes (apenas se a tabela estiver vazia)
if not session.query(Alimento).first():
    for nome, calorias, unidade, valores in alimentos_data:
        alimento = Alimento(
            nome_alimento=nome,
            unidade_padrao=unidade,
            calorias=calorias,
            id_categoria=categoria.id_categoria
        )
        session.add(alimento)
        session.flush()

        for nutriente_nome, qtd in valores.items():
            relacao = AlimentoNutriente(
                id_alimento=alimento.id_alimento,
                id_nutriente=nutrientes[nutriente_nome].id_nutriente,
                # **** CORREÇÃO APLICADA AQUI ****
                quantidade_por_100un=qtd
            )
            session.add(relacao)

    session.commit()
    print("Banco populado com sucesso")
else:
    print("O banco de dados já contém dados de alimentos.")