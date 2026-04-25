import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date


ESTOQUE_MINIMO_PADRAO = 30

CAT_EMOJIS = {
    "Alimentação": "🥩",
    "Higiene": "🧴",
    "Saúde": "💊",
    "Brinquedos": "🎾",
    "Acessórios": "🏠",
    "Serviços": "🛁",
}


class TelaDetalhes(tk.Toplevel):
    """Exibe todos os detalhes de um produto, com opções de Editar, Excluir e Vender."""

    def __init__(
        self,
        master,
        produto: dict,
        todos_produtos: list = None,
        callback_atualizar=None,
        callback_excluir=None,
    ):
        """
        :param master: janela pai (TelaConsulta ou qualquer Toplevel/Tk)
        :param produto: dict com as informações do produto
        :param todos_produtos: lista completa (usada para gerar novo ID ao salvar edição)
        :param callback_atualizar: função(produto_dict) chamada após edição salva
        :param callback_excluir: função(produto_id) chamada após exclusão confirmada
        """
        super().__init__(master)
        self.title("Detalhes do Produto")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.grab_set()

        self.produto = dict(produto)  # cópia local
        self.todos_produtos = todos_produtos or []
        self.callback_atualizar = callback_atualizar
        self.callback_excluir = callback_excluir

        self._build_ui()

    # ──────────────────────────────────────────────
    # CONSTRUÇÃO DA UI
    # ──────────────────────────────────────────────
    def _build_ui(self):
        BG = "#FFFFFF"
        FG = "#111111"
        BTN_BG = "#FFFFFF"

        p = self.produto
        est_min = p.get("estoque_minimo", ESTOQUE_MINIMO_PADRAO)
        estoque_baixo = int(p.get("quantidade", 0)) < est_min

        # ── Cabeçalho ──
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=12, pady=(10, 0))

        tk.Button(
            header, text="← VOLTAR", font=("Segoe UI", 10, "bold"),
            bg=BTN_BG, fg=FG, relief="solid", bd=1,
            cursor="hand2", command=self.destroy
        ).pack(side="left")

        tk.Button(
            header, text="🔍 NOVA CONSULTA", font=("Segoe UI", 10, "bold"),
            bg=BTN_BG, fg=FG, relief="solid", bd=1,
            cursor="hand2", command=self._nova_consulta
        ).pack(side="right")

        # ── Título ──
        tk.Label(
            self, text="🐾 DETALHES DO PRODUTO 🐾",
            font=("Segoe UI", 16, "bold"), bg=BG, fg=FG
        ).pack(pady=(8, 6))

        # ── Card ──
        card = tk.Frame(self, bg=BG, relief="solid", bd=1)
        card.pack(padx=14, pady=4, fill="both", expand=True)
        card.columnconfigure(1, weight=1)

        def linha(row, icone, label, valor_widget_ou_texto, col_span=1):
            tk.Label(card, text=icone, font=("Segoe UI", 13),
                     bg=BG).grid(row=row, column=0, padx=(12, 4), pady=6, sticky="nw")
            tk.Label(card, text=label, font=("Segoe UI", 11, "bold"),
                     bg=BG, fg=FG).grid(row=row, column=1, pady=6, sticky="nw")
            if isinstance(valor_widget_ou_texto, str):
                tk.Label(card, text=valor_widget_ou_texto, font=("Segoe UI", 11),
                         bg=BG, fg=FG, justify="left", wraplength=340
                         ).grid(row=row, column=2, padx=(0, 12), pady=6,
                                sticky="nw", columnspan=col_span)
            else:
                valor_widget_ou_texto.grid(
                    row=row, column=2, padx=(0, 12), pady=6,
                    sticky="nw", columnspan=col_span
                )

        # ID
        linha(0, "🏷", "ID do Produto:", str(p["id"]))

        # Categoria
        cat = p.get("categoria", "")
        emoji_cat = CAT_EMOJIS.get(cat, "")
        linha(1, "🥩", "Categoria:", f"{emoji_cat}  {cat}")

        # Nome
        linha(2, "🏷", "Nome:", p.get("nome", ""))

        # Preço
        linha(3, "$", "Preço:", f"R$ {float(p.get('preco', 0)):.2f}")

        # Quantidade + alerta
        qtd_frame = tk.Frame(card, bg=BG)
        tk.Label(
            qtd_frame, text=f"{p.get('quantidade', 0)} unidades",
            font=("Segoe UI", 11), bg=BG, fg=FG
        ).pack(anchor="w")

        if estoque_baixo:
            alerta = tk.Label(
                qtd_frame,
                text=f"⚠  ESTOQUE BAIXO (mínimo {est_min})",
                font=("Segoe UI", 10, "bold"),
                bg="#FFF3CD", fg="#856404",
                relief="solid", bd=1,
                padx=8, pady=4,
            )
            alerta.pack(anchor="w", pady=(4, 0))

        linha(4, "📦", "Quantidade:", qtd_frame)

        # Descrição
        desc_frame = tk.Frame(card, bg=BG)
        desc_text = tk.Text(
            desc_frame, font=("Segoe UI", 10), width=38, height=5,
            relief="solid", bd=1, wrap="word", state="disabled",
            bg="#FAFAFA"
        )
        desc_text.config(state="normal")
        desc_text.insert("end", p.get("descricao", ""))
        desc_text.config(state="disabled")
        desc_text.pack()
        linha(5, "📝", "Descrição:", desc_frame)

        # Data de cadastro
        linha(6, "📅", "Data de cadastro:", p.get("data_cadastro", "—"))

        # ── Botões de ação ──
        btns = tk.Frame(self, bg=BG)
        btns.pack(pady=10)

        for texto, cor_fg, cmd in [
            ("✏ EDITAR",   "#0D6EFD", self._editar),
            ("🗑 EXCLUIR",  "#DC3545", self._excluir),
            ("🛒 VENDER",   "#198754", self._vender),
        ]:
            tk.Button(
                btns, text=texto, font=("Segoe UI", 10, "bold"),
                bg=BTN_BG, fg=cor_fg, relief="solid", bd=1,
                cursor="hand2", width=12, command=cmd
            ).pack(side="left", padx=8, ipady=4)

    # ──────────────────────────────────────────────
    # AÇÕES
    # ──────────────────────────────────────────────
    def _nova_consulta(self):
        """Fecha detalhes e volta para consulta (que então reseta a busca)."""
        self.destroy()

    # ── EDITAR ──
    def _editar(self):
        """Abre janela de edição inline."""
        TelaEditar(
            self,
            produto=self.produto,
            callback_salvar=self._on_salvar_edicao
        )

    def _on_salvar_edicao(self, produto_atualizado: dict):
        self.produto = produto_atualizado
        # Atualiza tela (recria a UI)
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
        # Notifica TelaConsulta
        if self.callback_atualizar:
            self.callback_atualizar(self.produto)

    # ── EXCLUIR ──
    def _excluir(self):
        resp = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o produto:\n\n{self.produto['nome']}?",
            parent=self,
            icon="warning",
        )
        if resp:
            if self.callback_excluir:
                self.callback_excluir(self.produto["id"])
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!", parent=self)
            self.destroy()

    # ── VENDER ──
    def _vender(self):
        qtd_atual = int(self.produto.get("quantidade", 0))
        if qtd_atual <= 0:
            messagebox.showerror("Sem estoque", "Este produto está sem estoque!", parent=self)
            return

        qtd = simpledialog.askinteger(
            "Vender Produto",
            f"Produto: {self.produto['nome']}\nEstoque atual: {qtd_atual}\n\nQuantidade a vender:",
            parent=self, minvalue=1, maxvalue=qtd_atual
        )
        if qtd is None:
            return

        total = float(self.produto["preco"]) * qtd
        confirm = messagebox.askyesno(
            "Confirmar Venda",
            f"Vender {qtd} unidade(s) de:\n{self.produto['nome']}\n\n"
            f"Total: R$ {total:.2f}\n\nConfirmar?",
            parent=self
        )
        if confirm:
            self.produto["quantidade"] = qtd_atual - qtd
            if self.callback_atualizar:
                self.callback_atualizar(self.produto)
            messagebox.showinfo(
                "Venda Registrada",
                f"✅ Venda realizada!\n{qtd} un. → R$ {total:.2f}",
                parent=self
            )
            # Recarrega UI para refletir novo estoque
            for widget in self.winfo_children():
                widget.destroy()
            self._build_ui()


# ══════════════════════════════════════════════════════
# JANELA AUXILIAR DE EDIÇÃO
# ══════════════════════════════════════════════════════
class TelaEditar(tk.Toplevel):
    """Formulário de edição de produto (abre sobre TelaDetalhes)."""

    CATEGORIAS = ["Alimentação", "Higiene", "Saúde", "Brinquedos", "Acessórios", "Serviços"]

    def __init__(self, master, produto: dict, callback_salvar):
        super().__init__(master)
        self.title("Editar Produto")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.grab_set()

        self.produto = dict(produto)
        self.callback_salvar = callback_salvar
        self._build_ui()

    def _build_ui(self):
        BG = "#FFFFFF"
        FG = "#111111"
        p = self.produto

        tk.Label(self, text="🐾 EDITAR PRODUTO 🐾",
                 font=("Segoe UI", 14, "bold"), bg=BG, fg=FG).pack(pady=(12, 6))

        card = tk.Frame(self, bg=BG, relief="solid", bd=1)
        card.pack(padx=14, pady=4)
        card.columnconfigure(1, weight=1)

        def campo(row, icone, label, widget):
            tk.Label(card, text=icone, font=("Segoe UI", 12),
                     bg=BG).grid(row=row, column=0, padx=(10, 4), pady=6, sticky="w")
            tk.Label(card, text=label, font=("Segoe UI", 11, "bold"),
                     bg=BG).grid(row=row, column=1, sticky="w", pady=6)
            widget.grid(row=row, column=2, padx=(0, 10), pady=6, sticky="ew")

        # Categoria
        self.var_cat = tk.StringVar(value=p.get("categoria", self.CATEGORIAS[0]))
        opt_cat = tk.OptionMenu(card, self.var_cat, *self.CATEGORIAS)
        opt_cat.config(font=("Segoe UI", 10), bg="#FFFFFF", relief="solid", bd=1)
        campo(0, "🥩", "Categoria:", opt_cat)

        # Nome
        self.entry_nome = tk.Entry(card, font=("Segoe UI", 10), relief="solid", bd=1, width=34)
        self.entry_nome.insert(0, p.get("nome", ""))
        campo(1, "🏷", "Nome:", self.entry_nome)

        # Preço
        self.entry_preco = tk.Entry(card, font=("Segoe UI", 10), relief="solid", bd=1, width=34)
        self.entry_preco.insert(0, str(p.get("preco", "")))
        campo(2, "$", "Preço (R$):", self.entry_preco)

        # Quantidade
        self.entry_qtd = tk.Entry(card, font=("Segoe UI", 10), relief="solid", bd=1, width=34)
        self.entry_qtd.insert(0, str(p.get("quantidade", "")))
        campo(3, "📦", "Quantidade:", self.entry_qtd)

        # Estoque mínimo
        self.entry_est_min = tk.Entry(card, font=("Segoe UI", 10), relief="solid", bd=1, width=34)
        self.entry_est_min.insert(0, str(p.get("estoque_minimo", ESTOQUE_MINIMO_PADRAO)))
        campo(4, "⚠", "Est. Mínimo:", self.entry_est_min)

        # Descrição
        tk.Label(card, text="📝", font=("Segoe UI", 12), bg=BG
                 ).grid(row=5, column=0, padx=(10, 4), pady=6, sticky="nw")
        tk.Label(card, text="Descrição:", font=("Segoe UI", 11, "bold"),
                 bg=BG).grid(row=5, column=1, sticky="nw", pady=6)
        self.text_desc = tk.Text(card, font=("Segoe UI", 10), width=34, height=4,
                                 relief="solid", bd=1)
        self.text_desc.insert("end", p.get("descricao", ""))
        self.text_desc.grid(row=5, column=2, padx=(0, 10), pady=6)

        # Botões
        btns = tk.Frame(self, bg=BG)
        btns.pack(pady=10)

        tk.Button(btns, text="💾 SALVAR", font=("Segoe UI", 10, "bold"),
                  bg="#FFFFFF", fg="#198754", relief="solid", bd=1,
                  cursor="hand2", width=12, command=self._salvar
                  ).pack(side="left", padx=8, ipady=4)

        tk.Button(btns, text="🗑 LIMPAR", font=("Segoe UI", 10, "bold"),
                  bg="#FFFFFF", fg="#DC3545", relief="solid", bd=1,
                  cursor="hand2", width=12, command=self._limpar
                  ).pack(side="left", padx=8, ipady=4)

    def _salvar(self):
        nome = self.entry_nome.get().strip()
        preco_str = self.entry_preco.get().strip()
        qtd_str = self.entry_qtd.get().strip()
        est_min_str = self.entry_est_min.get().strip()
        desc = self.text_desc.get("1.0", "end").strip()

        if not nome:
            messagebox.showerror("Erro", "O nome do produto é obrigatório.", parent=self)
            return
        try:
            preco = float(preco_str.replace(",", "."))
            if preco < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido.", parent=self)
            return
        try:
            qtd = int(qtd_str)
            if qtd < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.", parent=self)
            return
        try:
            est_min = int(est_min_str)
            if est_min < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Estoque mínimo inválido.", parent=self)
            return

        produto_atualizado = dict(self.produto)
        produto_atualizado.update({
            "categoria": self.var_cat.get(),
            "nome": nome,
            "preco": preco,
            "quantidade": qtd,
            "estoque_minimo": est_min,
            "descricao": desc,
        })

        self.callback_salvar(produto_atualizado)
        messagebox.showinfo("Sucesso", "✅ Produto atualizado com sucesso!", parent=self)
        self.destroy()

    def _limpar(self):
        self.entry_nome.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.entry_qtd.delete(0, "end")
        self.entry_est_min.delete(0, "end")
        self.text_desc.delete("1.0", "end")


# ──────────────────────────────────────────────
# TESTE STANDALONE
# ──────────────────────────────────────────────
if __name__ == "__main__":
    PRODUTO_DEMO = {
        "id": 1,
        "nome": "Ração Royal Canin Maxi Adulto",
        "categoria": "Alimentação",
        "preco": 249.90,
        "quantidade": 25,
        "estoque_minimo": 30,
        "descricao": (
            "Ração super premium para cães adultos de porte grande. Sabor frango e arroz.\n"
            "✅ Sem corantes artificiais\n"
            "✅ Rico em ômega 3 e 6\n"
            "✅ Pró-bióticos para digestão\n"
            "✅ Peso líquido: 15kg"
        ),
        "data_cadastro": "06/04/2026",
    }

    root = tk.Tk()
    root.withdraw()
    TelaDetalhes(root, produto=PRODUTO_DEMO)
    root.mainloop()