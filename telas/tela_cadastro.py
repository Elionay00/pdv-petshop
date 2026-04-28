"""
Tela de Cadastro - PDV Pet Shop (CustomTkinter)
"""

import customtkinter as ctk
from tkinter import messagebox
import banco
from constantes import *


class TelaCadastro(ctk.CTkToplevel):
    """Tela de cadastro de produtos"""

    def __init__(self, master, mudar_tela_callback=None):
        super().__init__(master)
        self.title("Cadastrar Produto")
        self.geometry("600x650")
        self.resizable(False, False)
        self.grab_set()

        self.mudar_tela = mudar_tela_callback
        
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
            text="🐾 CADASTRAR PRODUTO 🐾",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COR_PRIMARIA
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=20, padx=20)
        
        # Nome
        ctk.CTkLabel(
            self.card, text="Nome:", 
            font=ctk.CTkFont(size=16)
        ).grid(row=1, column=0, pady=10, padx=20, sticky="e")
        
        self.nome_entry = ctk.CTkEntry(
            self.card, width=350, 
            placeholder_text="Ex: Ração Royal Canin"
        )
        self.nome_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")
        
        # Categoria
        ctk.CTkLabel(
            self.card, text="Categoria:", 
            font=ctk.CTkFont(size=16)
        ).grid(row=2, column=0, pady=10, padx=20, sticky="e")
        
        self.categoria_combo = ctk.CTkComboBox(
            self.card,
            values=["Alimentação", "Higiene", "Saúde", "Brinquedos", "Acessórios", "Serviços"],
            width=350
        )
        self.categoria_combo.grid(row=2, column=1, pady=10, padx=20, sticky="w")
        self.categoria_combo.set("Selecione...")
        
        # Preço
        ctk.CTkLabel(
            self.card, text="Preço (R$):", 
            font=ctk.CTkFont(size=16)
        ).grid(row=3, column=0, pady=10, padx=20, sticky="e")
        
        self.preco_entry = ctk.CTkEntry(
            self.card, width=350, 
            placeholder_text="Ex: 79.90"
        )
        self.preco_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")
        
        # Quantidade
        ctk.CTkLabel(
            self.card, text="Quantidade:", 
            font=ctk.CTkFont(size=16)
        ).grid(row=4, column=0, pady=10, padx=20, sticky="e")
        
        self.qtd_entry = ctk.CTkEntry(
            self.card, width=350, 
            placeholder_text="Ex: 50"
        )
        self.qtd_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")
        
        # Descrição
        ctk.CTkLabel(
            self.card, text="Descrição:", 
            font=ctk.CTkFont(size=16)
        ).grid(row=5, column=0, pady=10, padx=20, sticky="ne")
        
        self.desc_text = ctk.CTkTextbox(
            self.card, width=350, height=100
        )
        self.desc_text.grid(row=5, column=1, pady=10, padx=20, sticky="w")
        
        # Botões
        frame_botoes = ctk.CTkFrame(self.card, fg_color="transparent")
        frame_botoes.grid(row=6, column=0, columnspan=2, pady=30)
        
        btn_salvar = ctk.CTkButton(
            frame_botoes, text="💾 SALVAR", 
            fg_color=COR_PRIMARIA, width=120,
            command=self._salvar
        )
        btn_salvar.pack(side="left", padx=10)
        
        btn_limpar = ctk.CTkButton(
            frame_botoes, text="🗑️ LIMPAR", 
            fg_color=COR_TERCIARIA, width=120,
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

    def _salvar(self):
        """Salva o produto"""
        nome = self.nome_entry.get().strip()
        categoria = self.categoria_combo.get()
        preco = self.preco_entry.get().strip()
        qtd = self.qtd_entry.get().strip()
        descricao = self.desc_text.get("1.0", "end-1c").strip()
        
        if not nome:
            self.feedback.configure(text="⚠️ Nome é obrigatório!", text_color="red")
            return
        
        if categoria == "Selecione...":
            self.feedback.configure(text="⚠️ Selecione uma categoria!", text_color="red")
            return
        
        if not preco:
            self.feedback.configure(text="⚠️ Preço é obrigatório!", text_color="red")
            return
        
        if not qtd:
            self.feedback.configure(text="⚠️ Quantidade é obrigatória!", text_color="red")
            return
        
        try:
            preco_float = float(preco.replace(",", "."))
            if preco_float <= 0:
                raise ValueError
        except ValueError:
            self.feedback.configure(text="⚠️ Preço inválido!", text_color="red")
            return
        
        try:
            qtd_int = int(qtd)
            if qtd_int < 0:
                raise ValueError
        except ValueError:
            self.feedback.configure(text="⚠️ Quantidade inválida!", text_color="red")
            return
        
        try:
            banco.inserir_produto(nome, categoria, preco_float, qtd_int, descricao)
            self.feedback.configure(text="✅ Produto cadastrado com sucesso!", text_color="green")
            self._limpar()
            
            if messagebox.askyesno("Sucesso", "Produto cadastrado!\n\nDeseja cadastrar outro?"):
                self.nome_entry.focus()
            else:
                self._voltar()
                
        except Exception as e:
            self.feedback.configure(text=f"❌ Erro: {e}", text_color="red")

    def _limpar(self):
        """Limpa o formulário"""
        self.nome_entry.delete(0, "end")
        self.categoria_combo.set("Selecione...")
        self.preco_entry.delete(0, "end")
        self.qtd_entry.delete(0, "end")
        self.desc_text.delete("1.0", "end")
        self.feedback.configure(text="")

    def _voltar(self):
        """Volta para tela principal"""
        from telas.tela_principal import TelaPrincipal
        self.destroy()
        if self.mudar_tela:
            self.mudar_tela(TelaPrincipal)