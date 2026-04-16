"""
Tela Principal
"""

import customtkinter as ctk
from core.constantes import COR_PRIMARIA, COR_SECUNDARIA, COR_PERIGO, BOTAO_LARGO, BOTAO_ALTO, FONTE_BOTAO

class TelaPrincipal(ctk.CTkFrame):
    def __init__(self, parent, mudar_tela_callback):
        super().__init__(parent)
        self.mudar_tela = mudar_tela_callback
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0,1,2,3,4,5], weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self, 
            text="🐾 PDV PET SHOP 🐾",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        titulo.grid(row=0, column=0, pady=40)
        
        # Botão Cadastrar
        btn_cadastrar = ctk.CTkButton(
            self,
            text="🐶 CADASTRAR PRODUTO",
            font=FONTE_BOTAO,
            height=BOTAO_ALTO,
            width=BOTAO_LARGO,
            command=self.abrir_cadastro,
            fg_color=COR_PRIMARIA
        )
        btn_cadastrar.grid(row=1, column=0, pady=15)
        
        # Botão Consultar
        btn_consultar = ctk.CTkButton(
            self,
            text="🔍 CONSULTAR PRODUTOS",
            font=FONTE_BOTAO,
            height=BOTAO_ALTO,
            width=BOTAO_LARGO,
            command=self.abrir_consulta,
            fg_color=COR_SECUNDARIA
        )
        btn_consultar.grid(row=2, column=0, pady=15)
        
        # Botão Sair
        btn_sair = ctk.CTkButton(
            self,
            text="🚪 SAIR",
            font=FONTE_BOTAO,
            height=BOTAO_ALTO,
            width=BOTAO_LARGO,
            command=self.sair,
            fg_color=COR_PERIGO
        )
        btn_sair.grid(row=4, column=0, pady=15)
        
        # Label informativa
        lbl_info = ctk.CTkLabel(
            self,
            text=" Versão temporária",
            font=ctk.CTkFont(size=16),
            text_color="orange"
        )
        lbl_info.grid(row=5, column=0, pady=30)
    
    def abrir_cadastro(self):
        try:
            from telas.tela_cadastro import TelaCadastro
            self.mudar_tela(TelaCadastro)
        except ImportError:
            from tkinter import messagebox
            messagebox.showinfo("Aviso", "Tela de cadastro será implementada")
    
    def abrir_consulta(self):
        try:
            from telas.tela_consulta import TelaConsulta
            self.mudar_tela(TelaConsulta)
        except ImportError:
            from tkinter import messagebox
            messagebox.showinfo("Aviso", "Tela de consulta será implementada")
    
    def sair(self):
        self.master.master.destroy()