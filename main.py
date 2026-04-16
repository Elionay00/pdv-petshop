"""
PDV PET SHOP - Sistema de Auto Atendimento
Arquivo principal
"""

import customtkinter as ctk
from core import config
from database import banco
from core.constantes import LARGURA_JANELA, ALTURA_JANELA

class App:
    def __init__(self):
        # Criar a janela principal
        self.janela = ctk.CTk()
        self.janela.title("🐾 PDV PET SHOP - Auto Atendimento")
        self.janela.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}")
        
        # Centralizar a janela na tela
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)
        
        # Inicializar o banco de dados
        banco.criar_tabelas()
        
        # Carregar o tema salvo
        tema = config.obter_tema()
        ctk.set_appearance_mode(tema)
        ctk.set_default_color_theme("blue")
        
        # Frame principal que vai conter todas as telas
        self.frame_principal = ctk.CTkFrame(self.janela)
        self.frame_principal.grid(row=0, column=0, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=1)
        
        # Iniciar com a tela principal
        self.tela_atual = None
        self.mudar_tela(TelaPrincipal)
        
        # Configurar evento de fechar janela
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        
        # Iniciar o loop da aplicação
        self.janela.mainloop()
    
    def mudar_tela(self, nova_tela_class, **kwargs):
        """
        Troca a tela atual por uma nova tela
        
        Args:
            nova_tela_class: Classe da tela a ser criada
            **kwargs: Argumentos adicionais para a tela (ex: id_produto)
        """
        # Remover a tela atual se existir
        if self.tela_atual is not None:
            self.tela_atual.destroy()
        
        # Criar a nova tela
        self.tela_atual = nova_tela_class(
            self.frame_principal,
            self.mudar_tela,
            **kwargs
        )
        self.tela_atual.grid(row=0, column=0, sticky="nsew")
    
    def fechar_aplicacao(self):
        """Fecha a aplicação de forma segura"""
        if self.tela_atual:
            self.tela_atual.destroy()
        self.janela.destroy()

# Importar TelaPrincipal depois da classe App para evitar import circular
from telas.tela_principal import TelaPrincipal

# Ponto de entrada da aplicação
if __name__ == "__main__":
    try:
        app = App()
    except Exception as e:
        import traceback
        print(f"Erro fatal ao iniciar a aplicação: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")
        