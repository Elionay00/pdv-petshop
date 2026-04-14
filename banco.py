"""
Módulo temporário do banco de dados
"""

import sqlite3
import os

CAMINHO_BD = "dados/pdv.db"

def conectar():
    """Retorna conexão com o banco de dados"""
    os.makedirs("dados", exist_ok=True)
    return sqlite3.connect(CAMINHO_BD)

def criar_tabelas():
    """Cria a tabela produtos se não existir"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                descricao TEXT,
                data_cadastro DATE DEFAULT CURRENT_DATE
            )
        ''')
        conn.commit()
    print("✅ Banco de dados inicializado com sucesso!")

def inserir_produto(nome, categoria, preco, quantidade, descricao):
    """Insere um novo produto (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, categoria, preco, quantidade, descricao)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, categoria, float(preco), int(quantidade), descricao))
        conn.commit()
        return cursor.lastrowid

def listar_produtos():
    """Retorna todos os produtos (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, categoria, preco, quantidade FROM produtos ORDER BY id")
        return cursor.fetchall()

def buscar_produto(termo):
    """Busca produtos por ID ou nome (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        try:
            id_int = int(termo)
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_int,))
            resultado = cursor.fetchall()
            if resultado:
                return resultado
        except ValueError:
            pass
        
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{termo}%",))
        return cursor.fetchall()

def obter_produto_por_id(id_produto):
    """Retorna um produto específico (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        return cursor.fetchone()

def filtrar_por_categoria(categoria):
    """Retorna produtos de uma categoria (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, categoria, preco, quantidade FROM produtos WHERE categoria = ?", (categoria,))
        return cursor.fetchall()

def atualizar_quantidade(id_produto, nova_qtd):
    """Atualiza a quantidade de um produto (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_qtd, id_produto))
        conn.commit()
        return cursor.rowcount > 0

def excluir_produto(id_produto):
    """Exclui um produto (versão temporária)"""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conn.commit()
        return cursor.rowcount > 0