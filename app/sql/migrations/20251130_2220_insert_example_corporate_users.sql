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
$$;
