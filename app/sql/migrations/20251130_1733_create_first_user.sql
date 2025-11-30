INSERT INTO tb_government (department_name, email, password)
SELECT 'TI', 'admin@tecnologia.gov.br', 'tecnologia@123'
WHERE NOT EXISTS (
    SELECT 1 FROM tb_government WHERE id = 1
);
