def criar_tabelas():
    pass

def inserir_produto():
    pass

def popular():
    criar_tabelas()

    produtos = [
        ("Ração Premium Cães", "🍖 Alimentação", 120.0, 10, "Ração de alta qualidade"),
        ("Ração Gatos", "🍖 Alimentação", 90.0, 15, "Ração balanceada"),
        ("Coleira Antipulgas", "🏠 Acessórios", 45.0, 20, "Proteção contra pulgas"),
        ("Shampoo Pet", "🧴 Higiene", 25.0, 30, "Shampoo neutro"),
        ("Brinquedo Mordedor", "🎾 Brinquedos", 18.0, 40, "Resistente"),
        ("Areia para Gatos", "🧴 Higiene", 35.0, 25, "Alta absorção"),
        ("Cama Pet", "🏠 Acessórios", 80.0, 10, "Super confortável"),
        ("Caixa de Transporte", "🏠 Acessórios", 150.0, 5, "Ideal para viagens"),
        ("Petisco Canino", "🍖 Alimentação", 20.0, 50, "Snack saboroso"),
        ("Petisco Felino", "🍖 Alimentação", 22.0, 45, "Snack para gatos"),
        ("Escova de Pelos", "🧴 Higiene", 15.0, 35, "Remove pelos mortos"),
        ("Comedouro", "🏠 Acessórios", 30.0, 20, "Plástico resistente"),
        ("Bebedouro Automático", "🏠 Acessórios", 95.0, 12, "Água sempre fresca"),
        ("Tapete Higiênico", "🧴 Higiene", 55.0, 18, "Alta absorção"),
        ("Roupa Pet", "🏠 Acessórios", 60.0, 10, "Roupa confortável"),
        ("Guia para Passeio", "🏠 Acessórios", 40.0, 25, "Resistente"),
        ("Arranhador para Gatos", "🎾 Brinquedos", 70.0, 8, "Evita móveis danificados"),
        ("Bola Pet", "🎾 Brinquedos", 10.0, 60, "Diversão garantida"),
        ("Suplemento Vitaminico", "💊 Saúde", 65.0, 14, "Vitaminas essenciais"),
        ("Anti Pulgas Spray", "💊 Saúde", 50.0, 16, "Proteção extra"),
        ("Vermífugo", "💊 Saúde", 35.0, 20, "Controle de vermes")
    ]

    for _ in produtos:
        inserir_produto()

    print("✅ Banco populado com sucesso!")


if __name__ == "__main__":
    popular()