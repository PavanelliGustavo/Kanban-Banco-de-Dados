
CREATE OR REPLACE FUNCTION trg_tb_card_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE tb_card
       SET position = position - 1
     WHERE column_id = OLD.column_id
       AND position > OLD.position;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS after_delete_tb_card ON tb_card;
CREATE TRIGGER after_delete_tb_card
AFTER DELETE ON tb_card
FOR EACH ROW
EXECUTE FUNCTION trg_tb_card_after_delete();
