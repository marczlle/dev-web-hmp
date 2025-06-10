-- 1 Trigger: Logar calorias no registro diário ao adicionar alimento em uma refeição

CREATE OR REPLACE FUNCTION log_calorias_registro_diario()
RETURNS TRIGGER AS $$
DECLARE
    total_calorias INTEGER;
    usuario_id INTEGER;
    data_atual TEXT := TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD');
BEGIN
    -- Calcula calorias da refeição adicionada
    SELECT a.calorias * NEW.quantidade
    INTO total_calorias
    FROM alimento a
    WHERE a.id_alimento = NEW.id_alimento;

    -- Pega o usuário vinculado à refeição
    SELECT ur.id_usuario
    INTO usuario_id
    FROM usuario_refeicao ur
    WHERE ur.id_refeicao = NEW.id_refeicao
    LIMIT 1;

    -- Insere log
    INSERT INTO registro_diario(id_usuario, data, log)
    VALUES (usuario_id, data_atual, CONCAT('Foram adicionadas ', total_calorias, ' calorias na refeição ', NEW.id_refeicao, '.'));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_calorias
AFTER INSERT ON refeicao_alimento
FOR EACH ROW
EXECUTE FUNCTION log_calorias_registro_diario();



-- 2️ Trigger: Garantir que um alimento não tenha calorias negativas

CREATE OR REPLACE FUNCTION valida_calorias_alimento()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.calorias < 0 THEN
        RAISE EXCEPTION 'O valor de calorias não pode ser negativo.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valida_calorias
BEFORE INSERT OR UPDATE ON alimento
FOR EACH ROW
EXECUTE FUNCTION valida_calorias_alimento();



-- 3️ Trigger: Garantir que quantidade por 100 unidades seja positiva

CREATE OR REPLACE FUNCTION valida_quantidade_nutriente()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantidade_por_100un <= 0 THEN
        RAISE EXCEPTION 'A quantidade do nutriente deve ser maior que zero.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_valida_quantidade_nutriente
BEFORE INSERT OR UPDATE ON alimento_nutriente
FOR EACH ROW
EXECUTE FUNCTION valida_quantidade_nutriente();



-- 4 Trigger: Logar criação de novo usuário no registro diário

CREATE OR REPLACE FUNCTION log_novo_usuario()
RETURNS TRIGGER AS $$
DECLARE
    data_atual TEXT := TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD');
BEGIN
    INSERT INTO registro_diario(id_usuario, data, log)
    VALUES (NEW.id_usuario, data_atual, CONCAT('Novo usuário criado: ', NEW.nome));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_novo_usuario
AFTER INSERT ON usuario
FOR EACH ROW
EXECUTE FUNCTION log_novo_usuario();
