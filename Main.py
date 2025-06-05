import DAO
import DB
import Models

if __name__ == "__main__":
    dao = DAO.DAO()

    novo_usuario = Models.Usuario(nome="João da Silva")

    dao.adicionar_entidade(novo_usuario)
    teste1 = dao.obter_por_id(Models.Usuario, novo_usuario.id)
    teste2 = dao.obter_por_id(Models.Usuario, 1)

    print(teste1.nome)
    print(teste2.nome)

    novo_usuario.nome = "João da Silva Atualizado"
    usuario_atualizado = dao.atualizar_entidade(novo_usuario)

    print('-=-' * 20)
    print(usuario_atualizado.nome)
    print('-=-' * 20)

