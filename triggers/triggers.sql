-- Trigger 1: Logar calorias no registro diário ao adicionar alimento em uma refeição
CREATE TRIGGER trg_log_calorias
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


-- Trigger 2: Impedir que um alimento tenha calorias negativas (INSERT)
CREATE TRIGGER trg_valida_calorias_insert
BEFORE INSERT ON alimento
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.calorias < 0 THEN
            RAISE(ABORT, 'O valor de calorias não pode ser negativo.')
    END;
END;

-- Trigger 2 (UPDATE)
CREATE TRIGGER trg_valida_calorias_update
BEFORE UPDATE ON alimento
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.calorias < 0 THEN
            RAISE(ABORT, 'O valor de calorias não pode ser negativo.')
    END;
END;


-- Trigger 3: Garantir que quantidade por 100 unidades seja positiva (INSERT)
CREATE TRIGGER trg_valida_quantidade_nutriente_insert
BEFORE INSERT ON alimento_nutriente
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.quantidade_por_100un <= 0 THEN
            RAISE(ABORT, 'A quantidade do nutriente deve ser maior que zero.')
    END;
END;

-- Trigger 3 (UPDATE)
CREATE TRIGGER trg_valida_quantidade_nutriente_update
BEFORE UPDATE ON alimento_nutriente
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.quantidade_por_100un <= 0 THEN
            RAISE(ABORT, 'A quantidade do nutriente deve ser maior que zero.')
    END;                
END;


-- Trigger 4: Logar criação de novo usuário no registro diário
CREATE TRIGGER trg_log_novo_usuario
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
