"""
Tela de Venda - PDV Pet Shop (CustomTkinter)
"""

import customtkinter as ctk
import config
import banco
from constantes import *


class App:
    def __init__(self):
        print("Iniciando...")
        
        self.janela = ctk.CTk()
        self.janela.title("🐾 CENTRAL PET SHOP 🐾")
        self.janela.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
        
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)
        
        banco.criar_tabelas()
        
        tema = config.obter_tema()
        ctk.set_appearance_mode(tema)
        ctk.set_default_color_theme("blue")
        
        self.frame_principal = ctk.CTkFrame(self.janela)
        self.frame_principal.grid(row=0, column=0, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)
        
        self.tela_atual = None
        
        from telas.tela_principal import TelaPrincipal
        self.mudar_tela(TelaPrincipal)
        
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar)
        self.janela.mainloop()
    
    def mudar_tela(self, nova_tela_class, **kwargs):
        if self.tela_atual:
            self.tela_atual.destroy()
        
        self.tela_atual = nova_tela_class(
            self.frame_principal,
            self.mudar_tela,
            **kwargs
        )
        self.tela_atual.grid(row=0, column=0, sticky="nsew")
    
    def fechar(self):
        if self.tela_atual:
            self.tela_atual.destroy()
        self.janela.destroy()


if __name__ == "__main__":
    app = App()