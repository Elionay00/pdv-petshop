# biblioteca 
import customtkinter as ctk
import json  # ADICIONADO PARA SALVAR EM JSON

# tema 
ctk.set_appearance_mode("light")

ctk.set_default_color_theme("blue")


# classe 
class App(ctk.CTk):

    # função que roda o sistema
    def __init__(self):
        super().__init__()

        # lista de produtos (ADICIONADO)
        self.produtos = []
        self.carregar_dados()  # ADICIONADO

        # título 
        self.title("Cadastrar Produto")

        # tamanho da janela
        self.geometry("700x600")

        # cor de fundo 
        self.configure(fg_color="#f3f3f3")

        # TÍTULO PRINCIPAL 
        ctk.CTkLabel(
            self,
            text="🐾 CADASTRAR PRODUTO 🐾",
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 10))  # espaçamento em cima e embaixo

        # CARD (CAIXA BRANCA CENTRAL) 
        card = ctk.CTkFrame(
            self,
            fg_color="#ffffff",      # fundo branco
            corner_radius=10,        # borda arredondada
            border_width=1,          # largura da borda
            border_color="#ddd"      # cor da borda
        )
        card.pack(padx=40, pady=10, fill="both")  # espaçamento lateral

        # frame do formulário (fica dentro do card)
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=30, pady=20)

        # configuração de colunas 
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=3)

        #  FUNÇÃO PARA CRIAR CAMPO
        def campo(label, row):

            # label (texto do campo)
            ctk.CTkLabel(form, text=label, anchor="w").grid(
                row=row, column=0, sticky="w", pady=8
            )

            # campo de entrada
            entry = ctk.CTkEntry(
                form,
                width=320,
                height=35,
                corner_radius=8
            )
            entry.grid(row=row, column=1, pady=8, padx=(10, 0))

            return entry  # retorna o campo criado

        # CAMPO CATEGORIA 
        ctk.CTkLabel(form, text="🍖 Categoria:", anchor="w").grid(
            row=0, column=0, sticky="w", pady=8
        )

        # combobox lista de opções
        self.categoria = ctk.CTkComboBox(
            form,
            values=[
                "Alimentação",
                "Higiene e Limpeza",
                "Brinquedos",
                "Acessórios",
                "Saúde",
                "Estética",
                "Outros"
            ],
            width=320,
            height=35
        )
        self.categoria.grid(row=0, column=1, pady=8, padx=(10, 0))

        # valor padrão
        self.categoria.set("Alimentação")

        # OUTROS CAMPOS 
        self.nome = campo("🏷 Nome:", 1)
        self.preco = campo("💲 Preço (R$):", 2)
        self.qtd = campo("📦 Quantidade:", 3)

        # CAMPO DESCRIÇÃO 
        ctk.CTkLabel(form, text="📝 Descrição:", anchor="nw").grid(
            row=4, column=0, sticky="nw", pady=8
        )

        # campo de texto maior
        self.desc = ctk.CTkTextbox(
            form,
            width=320,
            height=80,
            corner_radius=8
        )
        self.desc.grid(row=4, column=1, pady=8, padx=(10, 0))

        # BOTÕES 
        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(pady=15)

        # botão salvar
        ctk.CTkButton(
            botoes,
            text="💾 SALVAR",
            width=160,
            height=40,
            fg_color="#4CAF50",
            command=self.salvar  # chama a função salvar
        ).pack(side="left", padx=10)

        # botão limpar
        ctk.CTkButton(
            botoes,
            text="🗑 LIMPAR",
            width=160,
            height=40,
            fg_color="#f44336",
            command=self.limpar  # chama a função limpar
        ).pack(side="left", padx=10)

        # MENSAGEM DE FEEDBACK 
        self.feedback = ctk.CTkLabel(self, text="")
        self.feedback.pack(pady=5)

    # FUNÇÃO SALVAR 
    def salvar(self):
        try:
            
            produto = {
                "categoria": self.categoria.get(),
                "nome": self.nome.get(),
                "preco": float(self.preco.get().replace(",", ".")),
                "quantidade": int(self.qtd.get()),
                "descricao": self.desc.get("1.0", "end").strip()
            }

            # ADICIONADO: salva na lista
            self.produtos.append(produto)

            # ADICIONADO: salva no arquivo JSON
            self.salvar_dados()

            # mostra mensagem de sucesso
            self.feedback.configure(
                text="✔ Produto cadastrado com sucesso!",
                text_color="green"
            )

            # limpa os campos
            self.limpar()

        except:
            # caso dê erro (ex: campo vazio ou inválido)
            self.feedback.configure(
                text="❌ Preencha corretamente",
                text_color="red"
            )

    # FUNÇÃO PARA SALVAR NO JSON
    def salvar_dados(self):
        with open("produtos.json", "w", encoding="utf-8") as f:
            json.dump(self.produtos, f, indent=4, ensure_ascii=False)

    # FUNÇÃO PARA CARREGAR DO JSON
    def carregar_dados(self):
        try:
            with open("produtos.json", "r", encoding="utf-8") as f:
                self.produtos = json.load(f)
        except:
            self.produtos = []

    # FUNÇÃO LIMPAR 
    def limpar(self):
        # limpa todos os campos
        self.nome.delete(0, "end")
        self.preco.delete(0, "end")
        self.qtd.delete(0, "end")
        self.desc.delete("1.0", "end")


# ===== EXECUÇÃO DO PROGRAMA =====
if __name__ == "__main__":
    app = App()   # cria a aplicação
    app.mainloop()  # mantém a janela aberta