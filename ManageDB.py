from DB import Engine, Base
import Models

def criar_tabelas():
    # Se alguma tabela não existir, ela será criada.
    # Se já existir, não será criada novamente.

    with Engine.connect() as connection: 
        # Estabelece uma conexão, dessa forma garante que ela seja fechada após o uso.
        try:
            Base.metadata.create_all(connection)
            connection.commit()
            # Realiza a operação.
        except Exception as e:
            print(f'❌ Erro ao criar tabelas: {e}')
            raise

def apagar_tabelas():
    # Apaga todas as tabelas do banco de dados.

    with Engine.connect() as connection:
        try:
            Base.metadata.drop_all(connection)
            connection.commit()
            # Realiza a operação.
        except Exception as e:
            print(f'❌ Erro ao dropar tabelas: {e}')
            raise
        

def mostrar_menu():
    # Mostra o menu de opções para o usuário.

    print('-=-' * 20)
    print('Choose an option:')
    print('1 - Create Tables')
    print('2 - Drop Tables')
    print('3 - Exit')
    print('-=-' * 20)

if __name__ == "__main__":
    # Interface no Terminal para Desenvolvimento.
    # Só pra facilitar criar e dropar tabelas no banco de dados.

    resposta = None

    print('-=-' * 20)
    print('Esse é o módulo de teste do BD.')

    while resposta != 3:
        if resposta is None:
            mostrar_menu()
            resposta = int(input('Option: '))
            print('-=-' * 20)
        if resposta == 1:
            criar_tabelas()
            print('-=-' * 20)
            print('✅ Tabelas criadas com sucesso.')
        elif resposta == 2:
            apagar_tabelas()
            print('-=-' * 20)
            print('✅ Tabelas dropadas com sucesso.')
        elif resposta == 3:
            break
        else:
            print(resposta)
            print('❌ Opção Invalida.')

        mostrar_menu()
        resposta = int(input('Option: '))
        print('-=-' * 20)

    print('👋 Saindo...')
