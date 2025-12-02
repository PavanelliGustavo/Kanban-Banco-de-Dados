CREATE OR REPLACE FUNCTION trg_tb_column_before_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.position <> OLD.position THEN
        -- Caso esteja movendo para frente (posição maior)
        IF NEW.position > OLD.position THEN
            UPDATE tb_column
               SET position = position - 1
             WHERE public_work_id = OLD.public_work_id
               AND position > OLD.position
               AND position <= NEW.position;
        ELSE
            -- Caso esteja movendo para trás (posição menor)
            UPDATE tb_column
               SET position = position + 1
             WHERE public_work_id = OLD.public_work_id
               AND position < OLD.position
               AND position >= NEW.position;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_update_tb_column ON tb_column;
CREATE TRIGGER before_update_tb_column
BEFORE UPDATE OF position ON tb_column
FOR EACH ROW
EXECUTE FUNCTION trg_tb_column_before_update();
