# Lista de Empresas
EMPRESAS_DB = [
    {"id": 1, "nome": "Construtora Horizonte Ltda", "cnpj": "12.345.678/0001-90", "email": "contato@horizonte.com.br"},
    {"id": 2, "nome": "Pavimentação Estrela do Sul", "cnpj": "98.765.432/0001-10", "email": "obras@estreladosul.com"},
    {"id": 3, "nome": "Engenharia Urbana Tech", "cnpj": "45.123.789/0001-55", "email": "adm@urbanatech.com.br"},
]

# Lista de Obras
# IMPORTANTE: Os IDs das obras (101, 102...) serão usados para filtrar as tarefas
OBRAS_DB = [
    {"id": 101, "empresa": "Construtora Horizonte Ltda", "nome": "Reforma da Escola Municipal", "local": "Centro - SP", "status": "Em Andamento", "data_inicio": "2023-01-15"},
    {"id": 102, "empresa": "Construtora Horizonte Ltda", "nome": "Construção de Ponte", "local": "Zona Norte - SP", "status": "Atrasado", "data_inicio": "2022-11-20"},
    {"id": 103, "empresa": "Construtora Horizonte Ltda", "nome": "Pavimentação Rua 10", "local": "Centro - SP", "status": "Concluído", "data_inicio": "2023-03-01"},
    {"id": 201, "empresa": "Pavimentação Estrela do Sul", "nome": "Ciclovia da Orla", "local": "Litoral - RJ", "status": "Em Andamento", "data_inicio": "2023-05-10"},
]

# Nova Lista: Tarefas/Cards do Kanban
# 'obra_id' conecta esta tarefa à obra específica acima
KANBAN_TASKS_DB = [
    # Tarefas da Obra 101 (Escola)
    {"id": 1, "obra_id": 101, "titulo": "Projeto Elétrico", "status": "Em Planejamento", "previsao": "10 dias"},
    {"id": 2, "obra_id": 101, "titulo": "Fundação", "status": "Concluído", "previsao": "-"},
    {"id": 3, "obra_id": 101, "titulo": "Alvenaria", "status": "Em Andamento", "previsao": "45% concluído"},
    {"id": 4, "obra_id": 101, "titulo": "Telhado", "status": "Em Planejamento", "previsao": "Aguardando material"},
    
    # Tarefas da Obra 102 (Ponte)
    {"id": 5, "obra_id": 102, "titulo": "Terraplanagem", "status": "Concluído", "previsao": "-"},
    {"id": 6, "obra_id": 102, "titulo": "Pilares de Sustentação", "status": "Em Verificação", "previsao": "Análise técnica"},
    
    # Tarefas da Obra 201 (Ciclovia)
    {"id": 7, "obra_id": 201, "titulo": "Pintura de Solo", "status": "Em Andamento", "previsao": "80% concluído"},
]