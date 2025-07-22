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
categoria = Categoria_Alimento(nome_categoria="Comida", descricao="Alimentos diversos")
session.add(categoria)
session.commit()

# Nutrientes
nutrientes = {
    "Gordura": Nutriente(nome_nutriente="Gordura", unidade_medida="g"),
    "Fibra": Nutriente(nome_nutriente="Fibra", unidade_medida="g"),
    "Proteína": Nutriente(nome_nutriente="Proteína", unidade_medida="g"),
    "Carboidrato": Nutriente(nome_nutriente="Carboidrato", unidade_medida="g"),
}
session.add_all(nutrientes.values())
session.commit()

# Alimentos com unidades realistas e nutrientes por porção
alimentos_data = [
    ("Frango Grelhado", 165, "100g", {"Proteína": 31, "Gordura": 3.6, "Carboidrato": 0, "Fibra": 0}),
    ("Arroz Integral", 111, "1 xícara", {"Proteína": 2.6, "Gordura": 0.9, "Carboidrato": 23, "Fibra": 1.8}),
    ("Feijão Preto", 132, "1 concha", {"Proteína": 8.9, "Gordura": 0.5, "Carboidrato": 23.7, "Fibra": 8.7}),
    ("Maçã", 52, "1 un", {"Proteína": 0.3, "Gordura": 0.2, "Carboidrato": 14, "Fibra": 2.4}),
    ("Ovo Cozido", 78, "1 un", {"Proteína": 6.3, "Gordura": 5.3, "Carboidrato": 0.6, "Fibra": 0}),
    ("Pão Integral", 69, "1 fatia", {"Proteína": 3.6, "Gordura": 1.1, "Carboidrato": 11.6, "Fibra": 1.9}),
    ("Iogurte Natural", 61, "1 copo (100ml)", {"Proteína": 3.5, "Gordura": 3.3, "Carboidrato": 4.7, "Fibra": 0}),
    ("Salmão", 208, "100g", {"Proteína": 20, "Gordura": 13, "Carboidrato": 0, "Fibra": 0}),
    ("Banana", 89, "1 un", {"Proteína": 1.1, "Gordura": 0.3, "Carboidrato": 23, "Fibra": 2.6}),
    ("Pizza de Pepperoni", 280, "1 fatia", {"Proteína": 11, "Gordura": 11, "Carboidrato": 32, "Fibra": 0.5}),
]

# Inserir alimentos e nutrientes
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
            quantidade_por_100un=int(qtd * 10)  # converter float → int de forma segura
        )
        session.add(relacao)

session.commit()
print("✨ Banco populado com sucesso com unidades realistas, ojou-sama~!")
