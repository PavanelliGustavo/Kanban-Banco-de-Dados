DO $$
BEGIN
    -- Adiciona a coluna apenas se não existir
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'tb_public_work'
          AND column_name = 'status'
    ) THEN
        ALTER TABLE tb_public_work
        ADD COLUMN status VARCHAR(20);
    END IF;

    -- Adiciona a constraint apenas se não existir
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'constraint_status'
          AND conrelid = 'tb_public_work'::regclass
    ) THEN
        ALTER TABLE tb_public_work
        ADD CONSTRAINT constraint_status
        CHECK (status IN ('PLANEJAMENTO', 'ANDAMENTO', 'CONCLUIDA', 'INTERROMPIDA'));
    END IF;
END;
$$ LANGUAGE plpgsql;