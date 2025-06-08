import DAO
import DB
import Models

if __name__ == "__main__":
    dao = DAO.DAO()

    strogonoff = Models.Refeicao(nome_refeicao="Strogonoff", descricao="Delicious beef strogonoff")
    joao = Models.Usuario(nome="João", email="joao@hotmail.com", senha="123456", genero="Masculino", altura=180, peso=75)

    # dao.adicionar_entidade(strogonoff)
    # dao.adicionar_entidade(joao)
    
    dao.adicionar_vinculo(Models.Usuario, Models.Refeicao, 2, 2)

    