import DAO
import DB
import Models
import setup_triggers

if __name__ == "__main__":
    dao = DAO.DAO()

    # -=-=-=-=- Teste de Trigger -=-=-=-=-

    setup_triggers.instalar_triggers()

    dao.adicionar_entidade(Models.Alimento(
        nome_alimento="Pinha",
        unidade_padrao="Unidade",
        calorias=-89,
        id_categoria=1
    ))

    # -=-=-=-=- Teste de Procedures -=-=-=-=-

    teste = dao.buscar_por_categoria("Frutas")

    for item in teste:
        print(item)

    #dao.calcular_total_nutrientes(1)

    #dao.atualizar_peso_altura(1, 190, 85)

    #dao.adicionar_alimento_em_refeicao(1, 7, 1)



    