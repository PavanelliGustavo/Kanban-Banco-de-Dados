DO $$
DECLARE
    v_corporate_id INT;
BEGIN
    -- Obter o corporate_id da Andrade Gutierrez
    SELECT id INTO v_corporate_id
    FROM tb_corporate
    WHERE email = 'contato@andradegutierrez.com';

    -- Obra 1
    IF NOT EXISTS (
        SELECT 1 FROM tb_public_work
        WHERE title = 'Duplicação da BR-101'
          AND corporate_id = v_corporate_id
    ) THEN
        CALL insert_public_work_with_activity(
            'Duplicação da BR-101',
            '2025-01-15',
            1,  -- location_id
            1,  -- government_id
            v_corporate_id,
            'ANDAMENTO',
            ARRAY[2,7]
        );
    END IF;

    -- Obra 2
    IF NOT EXISTS (
        SELECT 1 FROM tb_public_work
        WHERE title = 'Construção do Viaduto Central'
          AND corporate_id = v_corporate_id
    ) THEN
        CALL insert_public_work_with_activity(
            'Construção do Viaduto Central',
            '2025-02-01',
            2,
            1,
            v_corporate_id,
            'PLANEJAMENTO',
            ARRAY[6]
        );
    END IF;

    -- Obra 3
    IF NOT EXISTS (
        SELECT 1 FROM tb_public_work
        WHERE title = 'Linha de Metrô Norte'
          AND corporate_id = v_corporate_id
    ) THEN
        CALL insert_public_work_with_activity(
            'Linha de Metrô Norte',
            '2025-03-10',
            3,
            1,
            v_corporate_id,
            'ANDAMENTO',
            ARRAY[7]
        );
    END IF;

    -- Obra 4
    IF NOT EXISTS (
        SELECT 1 FROM tb_public_work
        WHERE title = 'Ponte sobre o Rio São Francisco'
          AND corporate_id = v_corporate_id
    ) THEN
        CALL insert_public_work_with_activity(
            'Ponte sobre o Rio São Francisco',
            '2025-04-05',
            4,
            1,
            v_corporate_id,
            'PLANEJAMENTO',
            ARRAY[2]
        );
    END IF;

    -- Obra 5
    IF NOT EXISTS (
        SELECT 1 FROM tb_public_work
        WHERE title = 'Terminal Rodoviário Interestadual'
          AND corporate_id = v_corporate_id
    ) THEN
        CALL insert_public_work_with_activity(
            'Terminal Rodoviário Interestadual',
            '2025-05-20',
            5,
            1,
            v_corporate_id,
            'ANDAMENTO',
            ARRAY[6,7]
        );
    END IF;
END;
$$ LANGUAGE plpgsql;