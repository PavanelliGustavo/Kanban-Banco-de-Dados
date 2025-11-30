INSERT INTO tb_government (user_name, department_name, email, password)
SELECT 'ADMIN', 'TI', 'admin@tecnologia.gov.br', 'tecnologia@123'
WHERE NOT EXISTS (
    SELECT 1 FROM tb_government WHERE id = 1
);
