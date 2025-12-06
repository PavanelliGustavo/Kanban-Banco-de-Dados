DO $$
BEGIN
    -- Adiciona a constraint apenas se não existir
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'unique_public_work_per_corporate'
          AND conrelid = 'tb_public_work'::regclass
    ) THEN
        ALTER TABLE tb_public_work
        ADD CONSTRAINT unique_public_work_per_corporate
        UNIQUE (title, corporate_id);
    END IF;
END;
$$ LANGUAGE plpgsql;