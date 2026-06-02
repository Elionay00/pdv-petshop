import sqlite3

DB_NAME = "petshop.db"

# Conexão
def conectar():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


# Criar a tabela
def criar_tabelas():
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                qtd INTEGER NOT NULL,
                descricao TEXT
            )
        """)
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")


# Inserir produtos
def inserir_produto(nome, categoria, preco, qtd, descricao):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO produtos (nome, 
            categoria, preco, qtd, descricao)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, categoria, preco, qtd, descricao))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")


# Listar produtos
def listar_produtos():
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produtos")

        produtos = cursor.fetchall()
        conn.close()
        return produtos

    except sqlite3.Error as e:
        print(f"Erro ao listar produtos: {e}")
        return []


# Buscar produto
def buscar_produto(termo):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM produtos
            WHERE nome LIKE ? OR categoria LIKE ?
        """, (f"%{termo}%", f"%{termo}%"))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    except sqlite3.Error as e:
        print(f"Erro ao buscar produto: {e}")
        return []


# Obter produto por ID
def obter_produto_por_id(produto_id):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM produtos WHERE id = ?", (produto_id,))

        produto = cursor.fetchone()
        conn.close()
        return produto

    except sqlite3.Error as e:
        print(f"Erro ao obter produto por ID: {e}")
        return None


# Filtrar produtos por categoria
def filtrar_por_categoria(categoria):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM produtos WHERE categoria = ?",
            (categoria,))

        produtos = cursor.fetchall()
        conn.close()
        return produtos

    except sqlite3.Error as e:
        print(f"Erro ao filtrar por categoria: {e}")
        return []


# Deletar produto
def deletar_produto(produto_id):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM produtos WHERE id = ?", (produto_id,))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao deletar produto: {e}")


# Atualizar produto
def atualizar_produto(produto_id, nome, categoria, preco, qtd, descricao):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE produtos
            SET nome = ?, categoria = ?, preco = ?, qtd = ?, descricao = ?
            WHERE id = ?
        """, (nome, categoria, preco, qtd, descricao, produto_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao atualizar produto: {e}")


# Atualizar estoque
def atualizar_estoque(produto_id, nova_qtd):
    """Atualiza a quantidade em estoque de um produto"""
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE produtos
            SET qtd = ?
            WHERE id = ?
        """, (nova_qtd, produto_id))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Erro ao atualizar estoque: {e}")
