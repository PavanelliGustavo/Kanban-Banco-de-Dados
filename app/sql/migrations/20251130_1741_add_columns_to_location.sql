DO $$
BEGIN
    -- Adiciona coluna uf se não existir
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'tb_location'
          AND column_name = 'uf'
    ) THEN
        ALTER TABLE tb_location ADD COLUMN uf VARCHAR(2) NOT NULL;
    END IF;

    -- Adiciona coluna city se não existir
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'tb_location'
          AND column_name = 'city'
    ) THEN
        ALTER TABLE tb_location ADD COLUMN city VARCHAR(50) NOT NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;
