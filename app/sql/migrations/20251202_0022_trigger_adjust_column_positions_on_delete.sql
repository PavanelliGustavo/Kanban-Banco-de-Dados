CREATE OR REPLACE FUNCTION trg_tb_column_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Ajustar posições após remoção
    UPDATE tb_column
       SET position = position - 1
     WHERE public_work_id = OLD.public_work_id
       AND position > OLD.position;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS after_delete_tb_column ON tb_column;
CREATE TRIGGER after_delete_tb_column
AFTER DELETE ON tb_column
FOR EACH ROW
EXECUTE FUNCTION trg_tb_column_after_delete();
