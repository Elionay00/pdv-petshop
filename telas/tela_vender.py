"""
Tela de Venda - PDV Pet Shop (CustomTkinter)
"""

import customtkinter as ctk
from tkinter import messagebox
import banco
from constantes import *
from telas.tela_principal import TelaPrincipal


class TelaVender(ctk.CTkToplevel):
    """Tela de venda de produtos"""

    def __init__(self, master, mudar_tela_callback=None):
        super().__init__(master)
        self.title("🐾 CENTRAL DE VENDA PET SHOP 🐾")
        self.geometry("600x650")
        self.resizable(False, False)
        self.grab_set()

        self.mudar_tela = mudar_tela_callback

        self.produtos = banco.listar_produtos()
        self.produto_atual = None
        self._build_ui()

    def _build_ui(self):
        """Constrói a interface"""

        # Grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Card principal
        self.card = ctk.CTkFrame(self, corner_radius=20)
        self.card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, weight=2)

        # Título
        titulo = ctk.CTkLabel(
            self.card,
            text="🛒 VENDER PRODUTO 🛒",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COR_TERCIARIA
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Produto
        ctk.CTkLabel(
            self.card, text="Produto:",
            font=ctk.CTkFont(size=16)
        ).grid(row=1, column=0, pady=10, padx=20, sticky="e")

        nomes_produtos = [p[1] for p in self.produtos]

        self.combo_produto = ctk.CTkComboBox(
            self.card,
            values=nomes_produtos if nomes_produtos else ["Nenhum produto"],
            width=350,
            command=self._selecionar_produto
        )

        self.combo_produto.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # Preço
        ctk.CTkLabel(
            self.card, text="Preço:",
            font=ctk.CTkFont(size=16)
        ).grid(row=2, column=0, pady=10, padx=20, sticky="e")

        self.lbl_preco = ctk.CTkLabel(
            self.card,
            text="R$ 0,00",
            font=ctk.CTkFont(size=16)
        )
        self.lbl_preco.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # Estoque
        ctk.CTkLabel(
            self.card,
            text="Estoque:",
            font=ctk.CTkFont(size=16)
        ).grid(row=3, column=0, pady=10, padx=20, sticky="e")

        self.lbl_estoque = ctk.CTkLabel(
            self.card,
            text="0",
            font=ctk.CTkFont(size=16)
        )
        self.lbl_estoque.grid(row=3, column=1, pady=10, padx=20, sticky="w")

            # Quantidade
        ctk.CTkLabel(
            self.card, text="Quantidade:",
            font=ctk.CTkFont(size=16)
        ).grid(row=4, column=0, pady=10, padx=20, sticky="e")

        self.entry_quantidade = ctk.CTkEntry(
            self.card, width=350,
            placeholder_text="Ex: 2"
        )
        self.entry_quantidade.grid(row=4, column=1, pady=10, padx=20, sticky="w")

        self.entry_quantidade.bind(
            "<KeyRelease>",
            lambda e: self._calcular_total()
        )

        # Total
        ctk.CTkLabel(
            self.card, text="Total:",
            font=ctk.CTkFont(size=16)
        ).grid(row=5, column=0, pady=10, padx=20, sticky="e")

        self.lbl_total = ctk.CTkLabel(
            self.card,
            text="R$ 0,00",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COR_SUCESSO
        )
        self.lbl_total.grid(row=5, column=1, pady=10, padx=20, sticky="w")

        if nomes_produtos:
            self.combo_produto.set(nomes_produtos[0])
            self._selecionar_produto(nomes_produtos[0])

        # Botões
        frame_botoes = ctk.CTkFrame(self.card, fg_color="transparent")
        frame_botoes.grid(row=6, column=0, columnspan=2, pady=30)

        btn_vender = ctk.CTkButton(
            frame_botoes, text="🛒 VENDER",
            fg_color=COR_TERCIARIA, width=120,
            command=self._vender
        )
        btn_vender.pack(side="left", padx=10)

        btn_limpar = ctk.CTkButton(
            frame_botoes, text="🗑️ LIMPAR",
            fg_color=COR_AVISO, width=120,
            command=self._limpar
        )
        btn_limpar.pack(side="left", padx=10)

        btn_voltar = ctk.CTkButton(
            frame_botoes, text="⬅️ VOLTAR",
            fg_color=COR_VOLTAR, width=120,
            command=self._voltar
        )
        btn_voltar.pack(side="left", padx=10)

        # Feedback
        self.feedback = ctk.CTkLabel(
            self.card, text="",
            font=ctk.CTkFont(size=12)
        )
        self.feedback.grid(row=7, column=0, columnspan=2, pady=10)

    def _selecionar_produto(self, nome_produto):
        for produto in self.produtos:
            if produto[1] == nome_produto:
                self.produto_atual = produto
                self.lbl_preco.configure(
                    text=f"R$ {produto[3]:.2f}".replace(".", ",")
                )
                self.lbl_estoque.configure(
                    text=str(produto[4])
                )
                self._calcular_total()
                break

    def _calcular_total(self):
        if not self.produto_atual:
            return
        try:

            qtd = int(self.entry_quantidade.get())
            total = qtd * self.produto_atual[3]
            self.lbl_total.configure(
                text=f"R$ {total:.2f}".replace(".", ",")
            )
        except:
            self.lbl_total.configure(
                text="R$ 0,00"
            )

    def _vender(self):
        if not self.produto_atual:
            self.feedback.configure(
                text="⚠️ Selecione um produto!",
                text_color="red"
            )
            return
        try:
            qtd_venda = int(
                self.entry_quantidade.get()
            )
        except ValueError:
            self.feedback.configure(
                text="⚠️ Quantidade inválida!",
                text_color="red"
            )
            return

        if qtd_venda <= 0:

            self.feedback.configure(
                text="⚠️ Quantidade deve ser maior que zero!",
                text_color="red"
            )
            return

        estoque = self.produto_atual[4]

        if qtd_venda > estoque:

            self.feedback.configure(
                text="⚠️ Estoque insuficiente!",
                text_color="red"
            )
            return

        novo_estoque = estoque - qtd_venda

        try:
            banco.atualizar_produto(
                self.produto_atual[0],
                self.produto_atual[1],
                self.produto_atual[2],
                self.produto_atual[3],
                novo_estoque,
                self.produto_atual[5]
            )

            self.feedback.configure(
                text="✅ Venda realizada com sucesso!", text_color="green")
            self._limpar()

            messagebox.showinfo(
                "Venda realizada","Venda realizada com sucesso!")

        except Exception as e:
            self.feedback.configure(text=f"❌ Erro: {e}", text_color="red")

    def _limpar(self):
        """Limpa o formulário"""
        self.entry_quantidade.delete(0, "end")
        self.lbl_total.configure(text="R$ 0,00" )
        self.feedback.configure(text="")
        self.lbl_estoque.configure(text="0")
        self.lbl_preco.configure(text="R$ 0,00")
        self.produto_atual = None

    def _voltar(self):
        """Volta para tela principal"""
        self.destroy()
        if self.mudar_tela:
            self.mudar_tela(TelaPrincipal)