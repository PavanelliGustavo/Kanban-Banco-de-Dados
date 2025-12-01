
CREATE OR REPLACE FUNCTION trg_tb_card_before_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Abrir espaço na coluna desejada
    -- Troque "+ 1" por "- 1" se quiser "reduzir em um" como mencionou
    UPDATE tb_card
       SET position = position + 1
     WHERE column_id = NEW.column_id
       AND position >= NEW.position;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_insert_tb_card ON tb_card;
CREATE TRIGGER before_insert_tb_card
BEFORE INSERT ON tb_card
FOR EACH ROW
EXECUTE FUNCTION trg_tb_card_before_insert();
