import DAO
import DB
import Models

if __name__ == "__main__":
    dao = DAO.DAO()

    strogonoff = Models.Refeicao(nome_refeicao="Strogonoff", descricao="Delicious beef strogonoff")
    arroz = Models.Alimento(nome_alimento="Arroz", unidade_padrao="xícara", calorias=200)
    tomate = Models.Alimento(nome_alimento="Tomate", unidade_padrao="g", calorias=20)
    carboidrato = Models.Nutriente(nome_nutriente="Carboidrato", unidade_medida="g")
    proteina = Models.Nutriente(nome_nutriente="Proteína", unidade_medida="g")
    gordura = Models.Nutriente(nome_nutriente="Gordura", unidade_medida="g")
    carne = Models.Categoria_Alimento(nome_categoria="Carne")
    picanha = Models.Alimento(nome_alimento="Picanha", unidade_padrao="g", calorias=300, categoria=carne)


    dao.adicionar_entidade(carne)
    dao.adicionar_entidade(picanha)



    