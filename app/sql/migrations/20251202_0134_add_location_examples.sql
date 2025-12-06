INSERT INTO tb_location (uf, city, address)
VALUES 
('SP', 'São Paulo', 'Rodovia BR-101, km 50'),
('RJ', 'Rio de Janeiro', 'Av. Brasil, 1000'),
('MG', 'Belo Horizonte', 'Praça Sete, Centro'),
('BA', 'Salvador', 'Av. Paralela, 200'),
('DF', 'Brasília', 'Esplanada dos Ministérios')
ON CONFLICT ON CONSTRAINT unique_location DO NOTHING;