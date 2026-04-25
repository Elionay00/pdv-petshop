import tkinter as tk
from tkinter import ttk, messagebox
from detalhes import TelaDetalhes


CATEGORIAS = {
    "Todos": "",
    "Alimentação": "Alimentação",
    "Higiene": "Higiene",
    "Saúde": "Saúde",
    "Brinquedos": "Brinquedos",
    "Acessórios": "Acessórios",
    "Serviços": "Serviços",
}

CAT_EMOJIS = {
    "Todos": "🥩",
    "Alimentação": "🥩",
    "Higiene": "🧴",
    "Saúde": "💊",
    "Brinquedos": "🎾",
    "Acessórios": "🏠",
    "Serviços": "🛁",
}

ESTOQUE_MINIMO = 30  # padrão geral (produtos com qty < 30 → Baixo)


class TelaConsulta(tk.Toplevel):
    """Tela de consulta / listagem de produtos."""

    def __init__(self, master, produtos: list, callback_voltar=None):
        """
        :param master: janela pai
        :param produtos: lista de dicts com chaves:
               id, nome, categoria, preco, quantidade, descricao,
               data_cadastro, estoque_minimo (opcional)
        :param callback_voltar: função chamada ao clicar em VOLTAR
        """
        super().__init__(master)
        self.title("Consultar Produtos")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.grab_set()

        self.produtos = produtos
        self.callback_voltar = callback_voltar
        self._filtro_categoria = ""
        self._produto_selecionado = None

        self._build_ui()
        self._carregar_tabela(self.produtos)

    # CONSTRUÇÃO DA UI
    def _build_ui(self):
        BG = "#FFFFFF"
        FG = "#111111"
        BTN_BG = "#FFFFFF"
        BTN_FG = "#111111"
        BTN_BD = "#111111"

        # Cabeçalho 
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=12, pady=(10, 0))

        btn_voltar = tk.Button(
            header, text="← VOLTAR", font=("Segoe UI", 10, "bold"),
            bg=BTN_BG, fg=BTN_FG, relief="solid", bd=1,
            cursor="hand2", command=self._voltar
        )
        btn_voltar.pack(side="left")

        btn_nova = tk.Button(
            header, text="🔍 NOVA CONSULTA", font=("Segoe UI", 10, "bold"),
            bg=BTN_BG, fg=BTN_FG, relief="solid", bd=1,
            cursor="hand2", command=self._nova_consulta
        )
        btn_nova.pack(side="right")

        # Título 
        tk.Label(
            self, text="🐾 CONSULTAR PRODUTOS 🐾",
            font=("Segoe UI", 16, "bold"), bg=BG, fg=FG
        ).pack(pady=(8, 6))

        # Card principal
        card = tk.Frame(self, bg=BG, relief="solid", bd=1)
        card.pack(padx=14, pady=4, fill="both", expand=True)

        # Barra de busca 
        busca_frame = tk.Frame(card, bg=BG)
        busca_frame.pack(padx=10, pady=(10, 4), fill="x")

        tk.Label(busca_frame, text="🔍  Pesquisar:", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=FG).pack(side="left")

        self.entry_busca = tk.Entry(
            busca_frame, font=("Segoe UI", 11), relief="solid", bd=1, width=30
        )
        self.entry_busca.insert(0, "Digite nome, categoria ou ID...")
        self.entry_busca.config(fg="#999999")
        self.entry_busca.bind("<FocusIn>", self._limpar_placeholder)
        self.entry_busca.bind("<FocusOut>", self._restaurar_placeholder)
        self.entry_busca.bind("<Return>", lambda e: self._buscar())
        self.entry_busca.pack(side="left", padx=8, ipady=4)

        tk.Button(
            busca_frame, text="BUSCAR", font=("Segoe UI", 10, "bold"),
            bg=BTN_BG, fg=BTN_FG, relief="solid", bd=1,
            cursor="hand2", command=self._buscar
        ).pack(side="left")

        # Filtros de categoria 
        filtro_frame = tk.Frame(card, bg=BG)
        filtro_frame.pack(padx=10, pady=4, fill="x")

        tk.Label(filtro_frame, text="🏷  Filtrar por:", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=FG).pack(side="left")

        self._btn_filtros = {}
        linha1 = tk.Frame(filtro_frame, bg=BG)
        linha1.pack(side="left", padx=4)

        cats_linha1 = ["Todos", "Alimentação", "Higiene", "Saúde"]
        cats_linha2 = ["Brinquedos", "Acessórios", "Serviços"]

        sub1 = tk.Frame(linha1, bg=BG)
        sub1.pack(anchor="w")
        for cat in cats_linha1:
            self._criar_botao_filtro(sub1, cat)

        sub2 = tk.Frame(linha1, bg=BG)
        sub2.pack(anchor="w", pady=2)
        for cat in cats_linha2:
            self._criar_botao_filtro(sub2, cat)

        self._btn_filtros["Todos"].config(
            relief="solid", bg="#E0E0E0"
        )

        # Tabela 
        tabela_frame = tk.Frame(card, bg=BG)
        tabela_frame.pack(padx=10, pady=(6, 4), fill="both", expand=True)

        colunas = ("id", "nome", "categoria", "preco", "qtd", "status")
        self.tree = ttk.Treeview(
            tabela_frame, columns=colunas, show="headings", height=8
        )

        headers = {
            "id": ("ID", 40),
            "nome": ("NOME", 180),
            "categoria": ("CATEGORIA", 100),
            "preco": ("PREÇO", 90),
            "qtd": ("QTD", 55),
            "status": ("STATUS", 80),
        }
        for col, (label, width) in headers.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")
        self.tree.column("nome", anchor="w")

        # Scrollbar vertical
        vsb = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Scrollbar horizontal
        hsb = ttk.Scrollbar(tabela_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tabela_frame.rowconfigure(0, weight=1)
        tabela_frame.columnconfigure(0, weight=1)

        # Tags de cor
        self.tree.tag_configure("baixo", background="#FFF3CD")
        self.tree.tag_configure("ok", background="#FFFFFF")

        # Duplo clique → detalhes
        self.tree.bind("<Double-1>", self._abrir_detalhes_duplo_clique)

        # Label de quantidade
        self.lbl_qtd = tk.Label(
            card, text="", font=("Segoe UI", 9),
            bg="#E8F5E9", fg="#2E7D32", relief="solid", bd=1
        )
        self.lbl_qtd.pack(padx=10, pady=(2, 8), fill="x")

        # Botões inferiores
        btns_frame = tk.Frame(self, bg=BG)
        btns_frame.pack(pady=10)

        for texto, cmd in [
            ("📋 DETALHES", self._abrir_detalhes),
            ("🔄 ATUALIZAR", self._atualizar),
            ("📊 ESTOQUE", self._ver_estoque),
        ]:
            tk.Button(
                btns_frame, text=texto, font=("Segoe UI", 10, "bold"),
                bg=BTN_BG, fg=BTN_FG, relief="solid", bd=1,
                cursor="hand2", width=14, command=cmd
            ).pack(side="left", padx=6, ipady=4)

    def _criar_botao_filtro(self, parent, cat):
        emoji = CAT_EMOJIS.get(cat, "")
        btn = tk.Button(
            parent,
            text=f"{emoji} {cat}",
            font=("Segoe UI", 9),
            bg="#FFFFFF", fg="#111111",
            relief="solid", bd=1,
            cursor="hand2",
            command=lambda c=cat: self._filtrar(c),
            padx=6, pady=2
        )
        btn.pack(side="left", padx=3, pady=1)
        self._btn_filtros[cat] = btn

    # LÓGICA
    def _carregar_tabela(self, lista: list):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in lista:
            est_min = p.get("estoque_minimo", ESTOQUE_MINIMO)
            baixo = int(p.get("quantidade", 0)) < est_min
            status = "⚠ Baixo" if baixo else "✅ OK"
            tag = "baixo" if baixo else "ok"

            cat_emoji = CAT_EMOJIS.get(p.get("categoria", ""), "")
            cat_display = f"{cat_emoji} {p.get('categoria', '')}"

            self.tree.insert(
                "", "end",
                iid=str(p["id"]),
                values=(
                    p["id"],
                    p["nome"],
                    cat_display,
                    f"R${float(p['preco']):.2f}",
                    p["quantidade"],
                    status,
                ),
                tags=(tag,),
            )

        total = len(lista)
        self.lbl_qtd.config(text=f"✅ {total} produto(s) encontrado(s)")

    def _buscar(self):
        termo = self.entry_busca.get().strip().lower()
        if termo == "digite nome, categoria ou id...":
            termo = ""

        resultado = []
        for p in self.produtos:
            cat = self._filtro_categoria
            if cat and p.get("categoria", "") != cat:
                continue
            if termo:
                if (
                    termo in str(p["id"]).lower()
                    or termo in p["nome"].lower()
                    or termo in p.get("categoria", "").lower()
                ):
                    resultado.append(p)
            else:
                resultado.append(p)

        self._carregar_tabela(resultado)

    def _filtrar(self, categoria: str):
        self._filtro_categoria = CATEGORIAS.get(categoria, "")
        # Destaque visual
        for cat, btn in self._btn_filtros.items():
            btn.config(bg="#FFFFFF")
        self._btn_filtros[categoria].config(bg="#E0E0E0")
        self._buscar()

    def _atualizar(self):
        self._filtro_categoria = ""
        for cat, btn in self._btn_filtros.items():
            btn.config(bg="#FFFFFF")
        self._btn_filtros["Todos"].config(bg="#E0E0E0")
        self.entry_busca.delete(0, "end")
        self.entry_busca.insert(0, "Digite nome, categoria ou ID...")
        self.entry_busca.config(fg="#999999")
        self._carregar_tabela(self.produtos)

    def _get_produto_selecionado(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela.", parent=self)
            return None
        pid = int(sel[0])
        for p in self.produtos:
            if p["id"] == pid:
                return p
        return None

    def _abrir_detalhes(self):
        p = self._get_produto_selecionado()
        if p:
            self._abrir_janela_detalhes(p)

    def _abrir_detalhes_duplo_clique(self, event):
        sel = self.tree.selection()
        if sel:
            pid = int(sel[0])
            for p in self.produtos:
                if p["id"] == pid:
                    self._abrir_janela_detalhes(p)
                    break

    def _abrir_janela_detalhes(self, produto):
        TelaDetalhes(
            self,
            produto=produto,
            todos_produtos=self.produtos,
            callback_atualizar=self._on_atualizar_produto,
            callback_excluir=self._on_excluir_produto,
        )

    def _on_atualizar_produto(self, produto_atualizado):
        """Chamado quando TelaDetalhes edita um produto."""
        for i, p in enumerate(self.produtos):
            if p["id"] == produto_atualizado["id"]:
                self.produtos[i] = produto_atualizado
                break
        self._atualizar()

    def _on_excluir_produto(self, produto_id):
        """Chamado quando TelaDetalhes exclui um produto."""
        self.produtos = [p for p in self.produtos if p["id"] != produto_id]
        self._atualizar()

    def _ver_estoque(self):
        baixo = [p for p in self.produtos
                 if int(p.get("quantidade", 0)) < p.get("estoque_minimo", ESTOQUE_MINIMO)]
        if not baixo:
            messagebox.showinfo("Estoque", "✅ Todos os produtos estão com estoque OK!", parent=self)
        else:
            nomes = "\n".join(
                f"• {p['nome']} → {p['quantidade']} un. (mín. {p.get('estoque_minimo', ESTOQUE_MINIMO)})"
                for p in baixo
            )
            messagebox.showwarning("⚠ Estoque Baixo", f"Produtos com estoque baixo:\n\n{nomes}", parent=self)

    def _nova_consulta(self):
        self._atualizar()

    def _voltar(self):
        self.destroy()
        if self.callback_voltar:
            self.callback_voltar()

    def _limpar_placeholder(self, event):
        if self.entry_busca.get() == "Digite nome, categoria ou ID...":
            self.entry_busca.delete(0, "end")
            self.entry_busca.config(fg="#111111")

    def _restaurar_placeholder(self, event):
        if not self.entry_busca.get():
            self.entry_busca.insert(0, "Digite nome, categoria ou ID...")
            self.entry_busca.config(fg="#999999")

# TESTE STANDALONE
if __name__ == "__main__":
    PRODUTOS_DEMO = [
        {"id": 1, "nome": "Ração Royal Canin Maxi Adulto", "categoria": "Alimentação",
         "preco": 249.90, "quantidade": 25, "estoque_minimo": 30,
         "descricao": "Ração super premium para cães adultos de porte grande. Sabor frango e arroz.\n✅ Sem corantes artificiais\n✅ Rico em ômega 3 e 6\n✅ Pró-bióticos para digestão\n✅ Peso líquido: 15kg",
         "data_cadastro": "06/04/2026"},
        {"id": 2, "nome": "Ração Premier Pet", "categoria": "Alimentação",
         "preco": 189.90, "quantidade": 50, "estoque_minimo": 30,
         "descricao": "Ração premium para cães adultos.", "data_cadastro": "06/04/2026"},
        {"id": 3, "nome": "Shampoo PetLove Antipulgas", "categoria": "Higiene",
         "preco": 39.90, "quantidade": 30, "estoque_minimo": 30,
         "descricao": "Shampoo antipulgas com ação prolongada.", "data_cadastro": "07/04/2026"},
        {"id": 4, "nome": "Vermífugo Vetnil", "categoria": "Saúde",
         "preco": 25.00, "quantidade": 15, "estoque_minimo": 30,
         "descricao": "Vermífugo de amplo espectro.", "data_cadastro": "07/04/2026"},
        {"id": 5, "nome": "Bolinha de Borracha", "categoria": "Brinquedos",
         "preco": 12.90, "quantidade": 100, "estoque_minimo": 30,
         "descricao": "Bolinha resistente para cães.", "data_cadastro": "08/04/2026"},
        {"id": 6, "nome": "Coleira Anti-pulgas", "categoria": "Acessórios",
         "preco": 45.00, "quantidade": 20, "estoque_minimo": 30,
         "descricao": "Coleira anti-pulgas com duração de 8 meses.", "data_cadastro": "08/04/2026"},
        {"id": 7, "nome": "Banho e Tosa (Pequeno)", "categoria": "Serviços",
         "preco": 55.00, "quantidade": 99, "estoque_minimo": 30,
         "descricao": "Serviço de banho e tosa para cães de pequeno porte.", "data_cadastro": "09/04/2026"},
    ]

    root = tk.Tk()
    root.withdraw()
    app = TelaConsulta(root, PRODUTOS_DEMO)
    root.mainloop()