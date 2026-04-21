"""
Tela Principal - PDV Pet Shop
Responsável: Gabrielly
"""

import customtkinter as ctk
from core.constantes import *

class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, parent, mudar_tela_callback):
        super().__init__(parent)
        self.mudar_tela = mudar_tela_callback
        
        # Configuração de layout centralizado
        self.grid_columnconfigure(0, weight=1)
        
        # --- Título ---
        self.titulo = ctk.CTkLabel(
            self, 
            text="🐾 PDV PET SHOP 🐾",
            font=FONTE_TITULO,
            text_color=COR_PRIMARIA
        )
        self.titulo.pack(pady=(50, 30)) # Espaçamento maior no topo
        
        # --- Container para os Botões (Organização) ---
        self.container_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.container_botoes.pack(expand=True, fill="both")

        # 1. Botão CADASTRAR (Verde)
        self.btn_cadastrar = ctk.CTkButton(
            self.container_botoes, 
            text="CADASTRAR",
            width=BOTAO_LARGO, 
            height=BOTAO_ALTO, 
            font=FONTE_BOTAO,
            fg_color=COR_PRIMARIA, 
            hover_color="#219150",
            command=lambda: self.mudar_tela("cadastro")
        )
        self.btn_cadastrar.pack(pady=10)

        # 2. Botão CONSULTAR (Azul)
        self.btn_consultar = ctk.CTkButton(
            self.container_botoes, 
            text="CONSULTAR",
            width=BOTAO_LARGO, 
            height=BOTAO_ALTO, 
            font=FONTE_BOTAO,
            fg_color=COR_SECUNDARIA, 
            hover_color="#2471a3", # Azul mais escuro no hover
            command=lambda: self.mudar_tela("consulta")
        )
        self.btn_consultar.pack(pady=10)

        # 3. Botão VENDER (Laranja)
        self.btn_vender = ctk.CTkButton(
            self.container_botoes, 
            text="VENDER",
            width=BOTAO_LARGO, 
            height=BOTAO_ALTO, 
            font=FONTE_BOTAO,
            fg_color=COR_TERCIARIA, 
            hover_color="#a04000", # Laranja mais escuro no hover
            command=lambda: self.mudar_tela("venda")
        )
        self.btn_vender.pack(pady=10)

        # 4. Botão ALTERAR TEMA (Cinza/Dark)
        self.btn_tema = ctk.CTkButton(
            self.container_botoes, 
            text="ALTERAR TEMA",
            width=BOTAO_LARGO, 
            height=BOTAO_ALTO, 
            font=FONTE_BOTAO,
            fg_color=COR_VOLTAR, 
            hover_color="#566573",
            command=self.alternar_tema
        )
        self.btn_tema.pack(pady=10)

        # 5. Botão SAIR (Vermelho)
        self.btn_sair = ctk.CTkButton(
            self.container_botoes, 
            text="SAIR",
            width=BOTAO_LARGO, 
            height=BOTAO_ALTO, 
            font=FONTE_BOTAO,
            fg_color=COR_PERIGO, 
            hover_color="#943126",
            command=self.quit
        )
        self.btn_sair.pack(pady=(10, 40))

    def alternar_tema(self):
        """Troca entre modo claro e escuro"""
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")