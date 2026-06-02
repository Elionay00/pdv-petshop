"""
Tela Principal - PDV Pet Shop
"""

import customtkinter as ctk
import config
from constantes import *


class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, parent, mudar_tela_callback):
        super().__init__(parent)
        self.mudar_tela = mudar_tela_callback
        
        self.grid_columnconfigure(0, weight=1)
        
        self.titulo = ctk.CTkLabel(
            self, text="🐾 CENTRAL PET SHOP 🐾",
            font=FONTE_TITULO, text_color=COR_PRIMARIA)
        self.titulo.pack(pady=(50, 30))
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both")

        self.btn_cadastrar = ctk.CTkButton(
            container, text="🐶 CADASTRAR",
            width=BOTAO_LARGO, height=BOTAO_ALTO,
            font=FONTE_BOTAO, fg_color=COR_PRIMARIA,
            command=self.abrir_cadastro
        )
        self.btn_cadastrar.pack(pady=10)

        self.btn_consultar = ctk.CTkButton(
            container, text="🔍 CONSULTAR",
            width=BOTAO_LARGO, height=BOTAO_ALTO,
            font=FONTE_BOTAO, fg_color=COR_SECUNDARIA,
            command=self.abrir_consulta
        )
        self.btn_consultar.pack(pady=10)

        self.btn_vender = ctk.CTkButton(
            container, text="🛒 VENDER",
            width=BOTAO_LARGO, height=BOTAO_ALTO,
            font=FONTE_BOTAO, fg_color=COR_TERCIARIA,
            command=self.abrir_venda
        )
        self.btn_vender.pack(pady=10)

        frame_final = ctk.CTkFrame(container, fg_color="transparent")
        frame_final.pack(pady=(15, 30))

        self.btn_tema = ctk.CTkButton(
            frame_final, text="🌙 TEMA",
            width=180, height=55,
            font=("Arial",18,"bold"), fg_color=COR_VOLTAR,
            command=self.alternar_tema
        )
        self.btn_tema.pack(side="left",padx=10)

        self.btn_sair = ctk.CTkButton(
            frame_final, text="🚪 SAIR",
            width=180, height=55,
            font=("Arial",18,"bold"), fg_color=COR_PERIGO,
            command=self.sair
        )
        self.btn_sair.pack(side="left",padx=10)
        
        self.atualizar_texto_tema()

    def abrir_cadastro(self):
        from telas.tela_cadastro import TelaCadastro
        self.mudar_tela(TelaCadastro)

    def abrir_consulta(self):
        from telas.tela_consulta import TelaConsulta
        self.mudar_tela(TelaConsulta)

    def abrir_venda(self):
        from telas.tela_vender import TelaVender
        self.mudar_tela(TelaVender)

    def alternar_tema(self):
        novo_tema = config.alternar_tema()
        ctk.set_appearance_mode(novo_tema)
        self.atualizar_texto_tema()

    def atualizar_texto_tema(self):
        tema = config.obter_tema()
        if tema == "dark":
            self.btn_tema.configure(text="☀️ TEMA")
        else:
            self.btn_tema.configure(text="🌙 TEMA")

    def sair(self):
        self.master.master.destroy()