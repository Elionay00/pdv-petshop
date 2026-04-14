"""
Arquivo de constantes do projeto PDV Pet Shop
Todos os membros devem usar estas constantes para padronização
"""

# ===== CORES =====
COR_PRIMARIA = "#2e7d32"      # Verde (Cadastrar)
COR_SECUNDARIA = "#1565c0"    # Azul (Consultar)
COR_TERCIARIA = "#f57c00"     # Laranja (Vender)
COR_PERIGO = "#c62828"        # Vermelho (Sair)
COR_VOLTAR = "#616161"        # Cinza (Voltar)
COR_SUCESSO = "#388e3c"       # Verde escuro (Sucesso)
COR_ERRO = "#d32f2f"          # Vermelho escuro (Erro)
COR_AVISO = "#ffa000"         # Laranja (Aviso)
COR_FUNDO = "#2b2b2b"         # Fundo padrão
COR_TEXTO = "white"           # Texto padrão

# ===== DIMENSÕES DA JANELA =====
LARGURA_JANELA = 1000
ALTURA_JANELA = 750

# ===== BOTÕES =====
BOTAO_LARGO = 400
BOTAO_ALTO = 90

BOTAO_MEDIO_LARGO = 200
BOTAO_MEDIO_ALTO = 45

BOTAO_PEQUENO_LARGO = 150
BOTAO_PEQUENO_ALTO = 40

# ===== CAMPOS =====
CAMPO_LARGURA = 350
CAMPO_ALTURA_TEXTO = 100

# ===== FONTES =====
FONTE_TITULO = ("Arial", 32, "bold")
FONTE_SUBTITULO = ("Arial", 24, "bold")
FONTE_BOTAO = ("Arial", 20, "bold")
FONTE_CAMPO = ("Arial", 18)
FONTE_TABELA = ("Arial", 14)

# ===== CATEGORIAS PET SHOP =====
CATEGORIAS = [
    ("🍖 Alimentação", "#795548"),
    ("🧴 Higiene", "#4fc3f7"),
    ("💊 Saúde", "#ef5350"),
    ("🎾 Brinquedos", "#ff9800"),
    ("🏠 Acessórios", "#9c27b0"),
    ("🛁 Serviços", "#26a69a")
]

# ===== MENSAGENS PADRÃO =====
MSG_CAMPO_VAZIO = "⚠️ Todos os campos obrigatórios devem ser preenchidos!"
MSG_PRECO_INVALIDO = "⚠️ Preço inválido! Use números (Ex: 10.50)"
MSG_QUANTIDADE_INVALIDA = "⚠️ Quantidade inválida! Use números inteiros (Ex: 100)"
MSG_SUCESSO_CADASTRO = "✅ Produto cadastrado com sucesso!"
MSG_ERRO_BANCO = "❌ Erro no banco de dados. Contate o suporte."
MSG_SEM_PRODUTOS = "📦 Nenhum produto cadastrado ainda."