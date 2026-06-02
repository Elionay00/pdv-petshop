"""
Tela de Detalhes - PDV Pet Shop (CustomTkinter)
"""

import customtkinter as ctk
from tkinter import messagebox
import banco
from constantes import *

class TelaDetalhes(ctk.CTkFrame):
    """Tela de detalhes do produto"""

    def __init__(self, parent, mudar_tela_callback, id_produto=None):
        super().__init__(parent)
        self.mudar_tela = mudar_tela_callback
        self.id_produto = id_produto
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(8, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self, 
            text="🐾 DETALHES DO PRODUTO 🐾",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_PRIMARIA
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=30)
        
        # Card
        card = ctk.CTkFrame(self, corner_radius=15)
        card.grid(row=1, column=0, columnspan=2, padx=40, pady=10, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=2)
        
        # Labels
        self.labels = {}
        infos = [
            ("📌 ID:", "id"),
            ("🏷️ Nome:", "nome"),
            ("📂 Categoria:", "categoria"),
            ("💰 Preço:", "preco"),
            ("📦 Quantidade:", "quantidade"),
            ("📝 Descrição:", "descricao")
        ]
        
        for i, (texto, chave) in enumerate(infos, start=1):
            lbl_titulo = ctk.CTkLabel(
                card, text=texto,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            lbl_titulo.grid(row=i, column=0, pady=10, padx=20, sticky="e")
            
            lbl_valor = ctk.CTkLabel(
                card, text="...", 
                font=ctk.CTkFont(size=16),
                wraplength=450, justify="left"
            )
            lbl_valor.grid(row=i, column=1, pady=10, padx=20, sticky="w")
            self.labels[chave] = lbl_valor
        
        # Botões
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.grid(row=2, column=0, columnspan=2, pady=30)
        
        btn_consulta = ctk.CTkButton(
            frame_botoes, text="🔍 IR PARA CONSULTA",
            command=self.ir_consulta, width=180,
            fg_color=COR_SECUNDARIA
        )
        btn_consulta.pack(side="left", padx=10)
        
        btn_voltar = ctk.CTkButton(
            frame_botoes, text="⬅️ VOLTAR",
            command=self.voltar_principal, width=150,
            fg_color=COR_VOLTAR
        )
        btn_voltar.pack(side="left", padx=10)
        
        # Status
        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.lbl_status.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Carregar dados
        if self.id_produto:
            self.carregar_detalhes()
        else:
            self.lbl_status.configure(text="❌ Nenhum produto selecionado!", text_color="red")
    
    def carregar_detalhes(self):
        """Carrega os detalhes do produto"""
        try:
            produto = banco.obter_produto_por_id(self.id_produto)
            
            if not produto:
                self.lbl_status.configure(text="❌ Produto não encontrado!", text_color="red")
                return
            
            self.labels["id"].configure(text=str(produto[0]))
            self.labels["nome"].configure(text=produto[1])
            self.labels["categoria"].configure(text=produto[2])
            self.labels["preco"].configure(text=f"R$ {produto[3]:.2f}".replace('.', ','))
            
            qtd = produto[4]
            if qtd <= 0:
                cor = "red"
                texto = f"{qtd} (ESGOTADO!)"
            elif qtd < 10:
                cor = "orange"
                texto = f"{qtd} (ESTOQUE BAIXO!)"
            else:
                cor = "green"
                texto = str(qtd)
            
            self.labels["quantidade"].configure(text=texto, text_color=cor)
            
            desc = produto[5] if produto[5] else "Sem descrição cadastrada."
            self.labels["descricao"].configure(text=desc)
            
            self.lbl_status.configure(text="✅ Detalhes carregados!", text_color="green")
            
        except Exception as e:
            self.lbl_status.configure(text=f"❌ Erro: {e}", text_color="red")
    
    def ir_consulta(self):
        """Vai para tela de consulta"""
        from telas.tela_consulta import TelaConsulta
        self.mudar_tela(TelaConsulta)
    
    def voltar_principal(self):
        """Volta para tela principal"""
        from telas.tela_principal import TelaPrincipal
        self.mudar_tela(TelaPrincipal)