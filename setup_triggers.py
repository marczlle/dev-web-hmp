from sqlalchemy import create_engine, text

def instalar_triggers():
    engine = create_engine('sqlite:///data.db')

    triggers = [
        # Trigger 1
        """
        CREATE TRIGGER IF NOT EXISTS trg_log_calorias
        AFTER INSERT ON refeicao_alimento
        FOR EACH ROW
        BEGIN
            INSERT INTO registro_diario(id_usuario, data, log)
            SELECT ur.id_usuario,
                   DATE('now'),
                   'Foram adicionadas ' || (a.calorias * NEW.quantidade) || ' calorias na refeição ' || NEW.id_refeicao || '.'
            FROM alimento a
            JOIN refeicao r ON r.id_refeicao = NEW.id_refeicao
            JOIN usuario_refeicao ur ON ur.id_refeicao = r.id_refeicao
            WHERE a.id_alimento = NEW.id_alimento
            LIMIT 1;
        END;
        """,

        # Trigger 2 (INSERT calorias negativas)
        """
        CREATE TRIGGER IF NOT EXISTS trg_valida_calorias_insert
        BEFORE INSERT ON alimento
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.calorias < 0 THEN
                    RAISE(ABORT, 'O valor de calorias não pode ser negativo.')
            END;
        END;
        """,

        # Trigger 2 (UPDATE calorias negativas)
        """
        CREATE TRIGGER IF NOT EXISTS trg_valida_calorias_update
        BEFORE UPDATE ON alimento
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.calorias < 0 THEN
                    RAISE(ABORT, 'O valor de calorias não pode ser negativo.')
            END;
        END;
        """,

        # Trigger 3 (INSERT nutriente)
        """
        CREATE TRIGGER IF NOT EXISTS trg_valida_quantidade_nutriente_insert
        BEFORE INSERT ON alimento_nutriente
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.quantidade_por_100un <= 0 THEN
                    RAISE(ABORT, 'A quantidade do nutriente deve ser maior que zero.')
            END;
        END;
        """,

        # Trigger 3 (UPDATE nutriente)
        """
        CREATE TRIGGER IF NOT EXISTS trg_valida_quantidade_nutriente_update
        BEFORE UPDATE ON alimento_nutriente
        FOR EACH ROW
        BEGIN
            SELECT CASE
                WHEN NEW.quantidade_por_100un <= 0 THEN
                    RAISE(ABORT, 'A quantidade do nutriente deve ser maior que zero.')
            END;
        END;
        """,

        # Trigger 4: novo usuário
        """
        CREATE TRIGGER IF NOT EXISTS trg_log_novo_usuario
        AFTER INSERT ON usuario
        FOR EACH ROW
        BEGIN
            INSERT INTO registro_diario(id_usuario, data, log)
            VALUES (
                NEW.id_usuario,
                DATE('now'),
                'Novo usuário criado: ' || NEW.nome
            );
        END;
        """
    ]

    with engine.begin() as conn:
        for i, trigger_sql in enumerate(triggers, start=1):
            print(f"Instalando trigger {i}...")
            conn.execute(text(trigger_sql))

    print("Db session fechou com sucesso. Todas as triggers foram instaladas!")

if __name__ == "__main__":
    instalar_triggers()
