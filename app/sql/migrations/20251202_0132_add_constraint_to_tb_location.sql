DO $$
BEGIN
    -- Adiciona a constraint apenas se não existir
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'unique_location'
          AND conrelid = 'tb_location'::regclass
    ) THEN
        ALTER TABLE tb_location
        ADD CONSTRAINT unique_location UNIQUE (uf, city, address);
    END IF;
END;
$$ LANGUAGE plpgsql;