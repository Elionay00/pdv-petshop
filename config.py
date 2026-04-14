"""
Módulo de configurações do sistema
Gerencia o tema (dark/light) salvando em arquivo JSON
"""

import json
import os

ARQUIVO_CONFIG = "dados/config.json"

def carregar_config():
    """Carrega as configurações salvas ou cria configuração padrão"""
    
    # Criar pasta dados se não existir
    if not os.path.exists("dados"):
        os.makedirs("dados")
    
    # Se arquivo não existe, criar padrão
    if not os.path.exists(ARQUIVO_CONFIG):
        config_padrao = {"tema": "dark"}
        salvar_config(config_padrao)
        return config_padrao
    
    # Tentar ler o arquivo
    try:
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro ao ler configuração: {e}")
        return {"tema": "dark"}

def salvar_config(config):
    """Salva as configurações em arquivo JSON"""
    try:
        # Criar pasta dados se não existir
        if not os.path.exists("dados"):
            os.makedirs("dados")
        
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar configuração: {e}")
        return False

def alternar_tema():
    """Alterna entre tema dark e light e salva a configuração"""
    config = carregar_config()
    tema_atual = config.get("tema", "dark")
    novo_tema = "light" if tema_atual == "dark" else "dark"
    config["tema"] = novo_tema
    salvar_config(config)
    return novo_tema

def obter_tema():
    """Retorna o tema atual salvo"""
    config = carregar_config()
    return config.get("tema", "dark")