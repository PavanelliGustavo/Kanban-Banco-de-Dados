# Lista de Empresas
EMPRESAS_DB = [
    {"id": 1, "nome": "Construtora Horizonte Ltda", "cnpj": "12.345.678/0001-90", "email": "contato@horizonte.com.br"},
    {"id": 2, "nome": "Pavimentação Estrela do Sul", "cnpj": "98.765.432/0001-10", "email": "obras@estreladosul.com"},
    {"id": 3, "nome": "Engenharia Urbana Tech", "cnpj": "45.123.789/0001-55", "email": "adm@urbanatech.com.br"},
]

# Lista de Obras
OBRAS_DB = [
    {"id": 101, "empresa": "Construtora Horizonte Ltda", "nome": "Reforma da Escola Municipal", "local": "Centro - SP", "status": "Em Andamento", "data_inicio": "2023-01-15"},
    {"id": 102, "empresa": "Construtora Horizonte Ltda", "nome": "Construção de Ponte", "local": "Zona Norte - SP", "status": "Atrasado", "data_inicio": "2022-11-20"},
    {"id": 103, "empresa": "Construtora Horizonte Ltda", "nome": "Pavimentação Rua 10", "local": "Centro - SP", "status": "Concluído", "data_inicio": "2023-03-01"},
    {"id": 201, "empresa": "Pavimentação Estrela do Sul", "nome": "Ciclovia da Orla", "local": "Litoral - RJ", "status": "Em Andamento", "data_inicio": "2023-05-10"},
]

# NOVA LISTA: Colunas do Kanban (Dinâmicas)
# Inicializamos com as colunas padrão para as obras existentes
COLUMNS_DB = [
    # Obra 101
    {"id": 1, "obra_id": 101, "titulo": "Em Planejamento", "posicao_visual": 1},
    {"id": 2, "obra_id": 101, "titulo": "Em Andamento", "posicao_visual": 2},
    {"id": 3, "obra_id": 101, "titulo": "Em Verificação", "posicao_visual": 3},
    {"id": 4, "obra_id": 101, "titulo": "Concluído", "posicao_visual": 4},
    # Obra 102
    {"id": 5, "obra_id": 102, "titulo": "Em Planejamento", "posicao_visual": 1},
    {"id": 6, "obra_id": 102, "titulo": "Em Andamento", "posicao_visual": 2},
    {"id": 7, "obra_id": 102, "titulo": "Em Verificação", "posicao_visual": 3},
    {"id": 8, "obra_id": 102, "titulo": "Concluído", "posicao_visual": 4},
    # Obra 201
    {"id": 9, "obra_id": 201, "titulo": "Em Planejamento", "posicao_visual": 1},
    {"id": 10, "obra_id": 201, "titulo": "Em Andamento", "posicao_visual": 2},
    {"id": 11, "obra_id": 201, "titulo": "Em Verificação", "posicao_visual": 3},
    {"id": 12, "obra_id": 201, "titulo": "Concluído", "posicao_visual": 4},
]

# Lista: Tarefas/Cards do Kanban
KANBAN_TASKS_DB = [
    # Tarefas da Obra 101 (Escola)
    {
        "id": 1, "obra_id": 101, "titulo": "Projeto Elétrico", "status": "Em Planejamento", "posicao": 1, "previsao": "10 dias",
        "responsavel": "Eng. Carlos Silva",
        "descricao_completa": "Elaboração de toda a planta baixa elétrica, incluindo dimensionamento de cargas para as novas salas de aula e laboratório de informática. Necessário aprovação dos bombeiros."
    },
    {
        "id": 2, "obra_id": 101, "titulo": "Fundação", "status": "Concluído", "posicao": 1, "previsao": "-",
        "responsavel": "Mestre de Obras João",
        "descricao_completa": "Concretagem das sapatas e vigas baldrame finalizada. Testes de resistência do concreto aprovados pelo laboratório externo."
    },
    {
        "id": 3, "obra_id": 101, "titulo": "Alvenaria", "status": "Em Andamento", "posicao": 1, "previsao": "45% concluído",
        "responsavel": "Equipe Alpha",
        "descricao_completa": "Levantamento das paredes do bloco B. O material (tijolos cerâmicos) já está 100% no canteiro de obras. Previsão de término da etapa em 2 semanas."
    },
    {
        "id": 4, "obra_id": 101, "titulo": "Telhado", "status": "Em Planejamento", "posicao": 2, "previsao": "Aguardando material",
        "responsavel": "Fornecedor TelhaNorte",
        "descricao_completa": "Estrutura metálica já foi orçada. Aguardando liberação de verba para compra das telhas termoacústicas."
    },
    # Tarefas da Obra 102 (Ponte)
    {
        "id": 5, "obra_id": 102, "titulo": "Terraplanagem", "status": "Concluído", "posicao": 1, "previsao": "-",
        "responsavel": "Op. Máquinas Pedro",
        "descricao_completa": "Nivelamento do terreno nas margens do rio concluído."
    },
    {
        "id": 6, "obra_id": 102, "titulo": "Pilares de Sustentação", "status": "Em Verificação", "posicao": 1, "previsao": "Análise técnica",
        "responsavel": "Eng. Estrutural Ana",
        "descricao_completa": "Pilares concretados. Aguardando período de cura e laudo de ultrassom para verificar integridade interna do concreto."
    },
    # Tarefas da Obra 201 (Ciclovia)
    {
        "id": 7, "obra_id": 201, "titulo": "Pintura de Solo", "status": "Em Andamento", "posicao": 1, "previsao": "80% concluído",
        "responsavel": "Equipe Pintura",
        "descricao_completa": "Aplicação da tinta vermelha e demarcação de faixas. Trecho 1 e 2 finalizados."
    },
]

# Lista: Documentos Oficiais
DOCUMENTS_DB = [
    {"id": 1, "obra_id": 101, "titulo": "Contrato de Prestação de Serviços - Nº 123/2023", "tipo": "PDF", "data": "2023-01-10", "caminho": "/docs/contrato_123.pdf"},
    {"id": 2, "obra_id": 101, "titulo": "Planta Baixa Aprovada", "tipo": "PDF", "data": "2023-01-12", "caminho": "/docs/planta_escola.pdf"},
    {"id": 3, "obra_id": 101, "titulo": "Licença Ambiental", "tipo": "PDF", "data": "2023-01-14", "caminho": "/docs/licenca_amb.pdf"},
    
    {"id": 4, "obra_id": 102, "titulo": "Estudo de Impacto de Vizinhança", "tipo": "DOCX", "data": "2022-11-01", "caminho": "/docs/eiv_ponte.docx"},
    {"id": 5, "obra_id": 102, "titulo": "Diário de Obras - Janeiro", "tipo": "PDF", "data": "2023-02-01", "caminho": "/docs/diario_jan.pdf"},
]
