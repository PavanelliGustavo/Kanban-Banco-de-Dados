
CREATE OR REPLACE FUNCTION trg_tb_card_before_update()
RETURNS TRIGGER AS $$
BEGIN
    -- Se coluna e posição não mudaram, não faz nada
    IF NEW.column_id = OLD.column_id AND NEW.position = OLD.position THEN
        RETURN NEW;
    END IF;

    IF NEW.column_id = OLD.column_id THEN
        -- Reordenação na MESMA coluna
        IF NEW.position < OLD.position THEN
            -- Moveu para cima: abre espaço acima
            UPDATE tb_card
               SET position = position + 1
             WHERE column_id = NEW.column_id
               AND id <> OLD.id
               AND position >= NEW.position
               AND position <  OLD.position;
        ELSIF NEW.position > OLD.position THEN
            -- Moveu para baixo: fecha espaço acima
            UPDATE tb_card
               SET position = position - 1
             WHERE column_id = NEW.column_id
               AND id <> OLD.id
               AND position <= NEW.position
               AND position >  OLD.position;
        END IF;

    ELSE
        -- Mudou de coluna: corrige ambas as colunas
        -- 1) Fecha buraco na coluna antiga (quem estava depois sobe 1)
        UPDATE tb_card
           SET position = position - 1
         WHERE column_id = OLD.column_id
           AND id <> OLD.id
           AND position > OLD.position;

        -- 2) Abre espaço na coluna nova (quem está em NEW.position ou depois desce 1)
        UPDATE tb_card
           SET position = position + 1
         WHERE column_id = NEW.column_id
           AND position >= NEW.position;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_update_tb_card ON tb_card;
CREATE TRIGGER before_update_tb_card
BEFORE UPDATE ON tb_card
FOR EACH ROW
EXECUTE FUNCTION trg_tb_card_before_update();
