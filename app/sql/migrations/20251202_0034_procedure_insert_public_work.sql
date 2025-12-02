CREATE OR REPLACE PROCEDURE insert_public_work_with_activity(
    p_title VARCHAR,
    p_description TEXT,
    p_email VARCHAR,
    p_password VARCHAR,
    p_field_ids INT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_corporate_id INT;
BEGIN
    -- Insere a empresa com todos os campos obrigatórios
    INSERT INTO tb_corporate (cnpj, name, email, password)
    VALUES (p_cnpj, p_name, p_email, p_password)
    RETURNING id INTO new_corporate_id;

    -- Verifica se foi passado ao menos um campo de atividade
    IF array_length(p_field_ids, 1) IS NULL THEN
        RAISE EXCEPTION 'É necessário informar ao menos um campo de atividade';
    END IF;

    -- Insere os vínculos na tabela relacional
    INSERT INTO tb_corporate_field_of_activity (corporate_id, field_of_activity_id)
    SELECT new_corporate_id, unnest(p_field_ids);
END;
$$;