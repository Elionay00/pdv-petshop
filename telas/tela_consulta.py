"""
Tela de Consulta - PDV Pet Shop (CustomTkinter)
"""

import customtkinter as ctk
from tkinter import messagebox
import banco
from constantes import *


class TelaConsulta(ctk.CTkToplevel):
    """Tela de consulta de produtos"""

    def __init__(self, master, mudar_tela_callback=None):
        super().__init__(master)
        self.title("Consultar Produtos")
        self.geometry("950x650")
        self.resizable(True, True)
        self.grab_set()

        self.mudar_tela = mudar_tela_callback
        self.produtos = []
        self.filtro_categoria = ""
        
        self.carregar_produtos()
        self._build_ui()
        self.carregar_tabela()

    def carregar_produtos(self):
        """Carrega produtos do banco"""
        try:
            dados = banco.listar_produtos()
            self.produtos = []
            for item in dados:
                self.produtos.append({
                    "id": item[0],
                    "nome": item[1],
                    "categoria": item[2],
                    "preco": item[3],
                    "quantidade": item[4],
                    "descricao": item[5] if len(item) > 5 else "",
                })
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

    def _build_ui(self):
        """Constrói a interface"""
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Cabeçalho
        cabecalho = ctk.CTkFrame(self)
        cabecalho.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        cabecalho.grid_columnconfigure(0, weight=1)
        
        btn_voltar = ctk.CTkButton(
            cabecalho, text="⬅️ VOLTAR", 
            width=120, command=self._voltar,
            fg_color=COR_VOLTAR
        )
        btn_voltar.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Título
        titulo = ctk.CTkLabel(
            self, text="🐾 CONSULTAR PRODUTOS 🐾",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_PRIMARIA
        )
        titulo.grid(row=1, column=0, pady=10)
        
        # Card principal
        card = ctk.CTkFrame(self, corner_radius=15)
        card.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        
        # Barra de busca
        frame_busca = ctk.CTkFrame(card)
        frame_busca.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_busca.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            frame_busca, text="🔍 Pesquisar:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_busca = ctk.CTkEntry(
            frame_busca, width=300, 
            placeholder_text="Digite ID ou nome..."
        )
        self.entry_busca.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_busca.bind("<Return>", lambda e: self._buscar())
        
        btn_buscar = ctk.CTkButton(
            frame_busca, text="BUSCAR", 
            width=100, command=self._buscar,
            fg_color=COR_SECUNDARIA
        )
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)
        
        # Filtros
        frame_filtros = ctk.CTkFrame(card)
        frame_filtros.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        frame_filtros.grid_columnconfigure(0, weight=1)
        
        btn_todos = ctk.CTkButton(
            frame_filtros, text="🥩 Todos",
            width=100, command=lambda: self._filtrar_categoria("")
        )
        btn_todos.grid(row=0, column=0, padx=5, pady=5)
        
        categorias = ["Alimentação", "Higiene", "Saúde", "Brinquedos", "Acessórios", "Serviços"]
        for i, cat in enumerate(categorias, start=1):
            btn = ctk.CTkButton(
                frame_filtros, text=f"{cat[:1]} {cat}",
                width=100, command=lambda c=cat: self._filtrar_categoria(c)
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        # Tabela (usando CTkScrollableFrame com labels para simular tabela)
        frame_tabela = ctk.CTkScrollableFrame(card)
        frame_tabela.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        frame_tabela.grid_columnconfigure(0, weight=1)
        
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(frame_tabela)
        header_frame.pack(fill="x", pady=2)
        
        headers = ["ID", "NOME", "CATEGORIA", "PREÇO", "QTD"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                header_frame, text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100 if i == 0 else 150
            )
            lbl.pack(side="left", padx=5, expand=True if i > 0 else False)
        
        # Container para linhas
        self.linhas_container = ctk.CTkFrame(frame_tabela)
        self.linhas_container.pack(fill="both", expand=True)
        
        # Label de status
        self.lbl_status = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12)
        )
        self.lbl_status.grid(row=3, column=0, pady=10)

    def carregar_tabela(self, produtos=None):
        """Carrega os produtos na tabela"""
        # Limpar linhas existentes
        for widget in self.linhas_container.winfo_children():
            widget.destroy()
        
        dados = produtos if produtos is not None else self.produtos
        
        if not dados:
            lbl_vazio = ctk.CTkLabel(
                self.linhas_container, text="📦 Nenhum produto encontrado",
                font=ctk.CTkFont(size=16)
            )
            lbl_vazio.pack(pady=50)
            self.lbl_status.configure(text="📦 0 produto(s) encontrado(s)")
            return
        
        for produto in dados:
            linha = ctk.CTkFrame(self.linhas_container)
            linha.pack(fill="x", pady=2, padx=5)
            
            # Bind de duplo clique
            def callback(p=produto):
                self._abrir_detalhes(p)
            
            lbl_id = ctk.CTkLabel(linha, text=str(produto["id"]), width=50)
            lbl_id.pack(side="left", padx=5)
            lbl_id.bind("<Button-1>", lambda e, p=produto: self._abrir_detalhes(p))
            
            lbl_nome = ctk.CTkLabel(linha, text=produto["nome"], width=200, anchor="w")
            lbl_nome.pack(side="left", padx=5, fill="x", expand=True)
            lbl_nome.bind("<Button-1>", lambda e, p=produto: self._abrir_detalhes(p))
            
            lbl_cat = ctk.CTkLabel(linha, text=produto["categoria"], width=120)
            lbl_cat.pack(side="left", padx=5)
            lbl_cat.bind("<Button-1>", lambda e, p=produto: self._abrir_detalhes(p))
            
            lbl_preco = ctk.CTkLabel(linha, text=f"R$ {produto['preco']:.2f}".replace('.', ','), width=100)
            lbl_preco.pack(side="left", padx=5)
            lbl_preco.bind("<Button-1>", lambda e, p=produto: self._abrir_detalhes(p))
            
            qtd = produto["quantidade"]
            cor = "green" if qtd >= 10 else ("orange" if qtd > 0 else "red")
            lbl_qtd = ctk.CTkLabel(linha, text=str(qtd), width=60, text_color=cor)
            lbl_qtd.pack(side="left", padx=5)
            lbl_qtd.bind("<Button-1>", lambda e, p=produto: self._abrir_detalhes(p))
        
        self.lbl_status.configure(text=f"✅ {len(dados)} produto(s) encontrado(s)", text_color="green")

    def _buscar(self):
        """Busca produtos"""
        termo = self.entry_busca.get().strip().lower()
        if not termo:
            self.carregar_tabela()
            return
        
        resultado = [p for p in self.produtos if termo in str(p["id"]).lower() or termo in p["nome"].lower()]
        self.carregar_tabela(resultado)

    def _filtrar_categoria(self, categoria):
        """Filtra por categoria"""
        if not categoria:
            self.carregar_tabela()
        else:
            resultado = [p for p in self.produtos if p["categoria"] == categoria]
            self.carregar_tabela(resultado)

    def _abrir_detalhes(self, produto):
        """Abre tela de detalhes"""
        from telas.tela_detalhes import TelaDetalhes
        self.destroy()
        if self.mudar_tela:
            self.mudar_tela(TelaDetalhes, id_produto=produto["id"])

    def _voltar(self):
        """Volta para tela principal"""
        from telas.tela_principal import TelaPrincipal
        self.destroy()
        if self.mudar_tela:
            self.mudar_tela(TelaPrincipal)