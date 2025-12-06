DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM tb_corporate WHERE email = 'contato@andradegutierrez.com') THEN
        CALL insert_corporate_with_activity(
            '17262213000194',
            'Andrade Gutierrez',
            'contato@andradegutierrez.com',
            'SenhaAG2025',
            ARRAY[2, 6, 7]
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tb_corporate WHERE email = 'contato@camargocorrea.com') THEN
        CALL insert_corporate_with_activity(
            '61522512000102',
            'Camargo Corrêa Infra',
            'contato@camargocorrea.com',
            'SenhaCC2025',
            ARRAY[5]
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tb_corporate WHERE email = 'contato@petrobras.com.br') THEN
        CALL insert_corporate_with_activity(
            '33000167000101',
            'Petrobras - Petróleo Brasileiro S.A.',
            'contato@petrobras.com.br',
            'senhaPetro123',
            ARRAY[6, 13, 14]
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tb_corporate WHERE email = 'contato@vale.com') THEN
        CALL insert_corporate_with_activity(
            '33592510000154',
            'Vale S.A.',
            'contato@vale.com',
            'senhaVale456',
            ARRAY[2, 3, 18, 33]
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM tb_corporate WHERE email = 'contato@construcap.com') THEN
        CALL insert_corporate_with_activity(
            '61584223000138',
            'Construcap',
            'contato@construcap.com',
            'SenhaConstrucap2025',
            ARRAY[34, 36]
        );
    END IF;
END;
$$ LANGUAGE plpgsql;