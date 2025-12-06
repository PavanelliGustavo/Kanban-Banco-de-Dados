CREATE OR REPLACE VIEW vw_public_works_all_cards_in_last_column AS
SELECT pw.*
FROM tb_public_work pw
WHERE 
    EXISTS (
        SELECT 1 
        FROM tb_card c 
        WHERE c.public_work_id = pw.id
    )
    AND 
    NOT EXISTS (
        SELECT 1
        FROM tb_card c
        JOIN tb_column col ON col.id = c.column_id
        WHERE c.public_work_id = pw.id
          AND col.id <> (
              SELECT id
              FROM tb_column
              WHERE public_work_id = pw.id
              ORDER BY position DESC
              LIMIT 1
          )
    );