CREATE OR REPLACE PROCEDURE insert_public_work_with_activity(
    p_title VARCHAR,
    p_start_date DATE,
    p_location_id INT,
    p_government_id INT,
    p_corporate_id INT,
    p_status VARCHAR,
    p_field_ids INT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_public_work_id INT;
BEGIN
    -- Verifica se foi passado ao menos um campo de atividade
    IF array_length(p_field_ids, 1) IS NULL THEN
        RAISE EXCEPTION 'É necessário informar ao menos um campo de atividade para a obra pública';
    END IF;

    -- Insere a obra pública
    INSERT INTO tb_public_work (title, start_date, location_id, government_id, corporate_id, status)
    VALUES (p_title, p_start_date, p_location_id, p_government_id, p_corporate_id, p_status)
    RETURNING id INTO new_public_work_id;

    -- Insere os vínculos na tabela relacional
    INSERT INTO tb_public_work_field_of_activity (public_work_id, field_of_activity_id)
    SELECT new_public_work_id, unnest(p_field_ids);
END;
$$;