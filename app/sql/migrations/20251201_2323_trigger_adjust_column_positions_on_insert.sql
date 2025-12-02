CREATE OR REPLACE FUNCTION trg_tb_column_before_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Abrir espaço na posição desejada dentro do board
    UPDATE tb_column
       SET position = position + 1
     WHERE public_work_id = NEW.public_work_id
       AND position >= NEW.position;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_insert_tb_column ON tb_column;
CREATE TRIGGER before_insert_tb_column
BEFORE INSERT ON tb_column
FOR EACH ROW
EXECUTE FUNCTION trg_tb_column_before_insert();
