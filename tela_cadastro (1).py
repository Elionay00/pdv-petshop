import tkinter as tk
from tkinter import ttk, messagebox

# protudos banco de dados
banco_produtos = []


class TelaCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastrar Produto")
        self.root.geometry("600x500")

        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        #TÍTULO
        titulo = tk.Label(frame, text="🐾 CADASTRAR PRODUTO 🐾", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # FORMULÁRIO
        form = tk.Frame(frame)
        form.pack(pady=10)

        # Nome
        tk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(form, width=40)
        self.nome_entry.grid(row=0, column=1, pady=5)

        # Categoria
        tk.Label(form, text="Categoria:").grid(row=1, column=0, sticky="w")
        self.categoria = ttk.Combobox(
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
            state="readonly"
        )
        self.categoria.grid(row=1, column=1, pady=5)
        self.categoria.current(0)

        # ====== PREÇO (COM VALIDAÇÃO FLOAT) ======
        tk.Label(form, text="Preço (R$):").grid(row=2, column=0, sticky="w")

        vcmd_preco = (self.root.register(self.validar_float), "%P")

        self.preco_entry = tk.Entry(
            form,
            validate="key",
            validatecommand=vcmd_preco
        )
        self.preco_entry.grid(row=2, column=1, pady=5)

        # ====== QUANTIDADE (SÓ INTEIRO) ======
        tk.Label(form, text="Quantidade:").grid(row=3, column=0, sticky="w")

        vcmd_int = (self.root.register(self.validar_int), "%P")

        self.qtd_entry = tk.Entry(
            form,
            validate="key",
            validatecommand=vcmd_int
        )
        self.qtd_entry.grid(row=3, column=1, pady=5)

        # Descrição
        tk.Label(form, text="Descrição:").grid(row=4, column=0, sticky="nw")
        self.desc_text = tk.Text(form, width=30, height=5)
        self.desc_text.grid(row=4, column=1, pady=5)

        # ====== BOTÕES ======
        botoes = tk.Frame(frame)
        botoes.pack(pady=15)

        tk.Button(botoes, text="SALVAR", width=12, command=self.salvar).grid(row=0, column=0, padx=5)
        tk.Button(botoes, text="LIMPAR", width=12, command=self.limpar).grid(row=0, column=1, padx=5)
        tk.Button(botoes, text="VOLTAR", width=12, command=self.voltar).grid(row=0, column=2, padx=5)

        # Feedback
        self.feedback = tk.Label(frame, text="", fg="green")
        self.feedback.pack()

    # ====== VALIDAÇÃO FLOAT (PREÇO) ======
    def validar_float(self, valor):
        if valor == "":
            return True
        try:
            float(valor.replace(",", "."))
            return True
        except ValueError:
            return False

    # ====== VALIDAÇÃO INT (QUANTIDADE) ======
    def validar_int(self, valor):
        if valor == "":
            return True
        return valor.isdigit()

    # ====== VALIDAÇÃO FINAL ======
    def validar(self):
        try:
            nome = self.nome_entry.get().strip()
            if not nome:
                raise ValueError("Nome obrigatório")

            preco = float(self.preco_entry.get().replace(",", "."))
            qtd = int(self.qtd_entry.get())

            return nome, preco, qtd

        except ValueError as e:
            messagebox.showerror("Erro", f"Erro de validação: {e}")
            return None

    # ====== SALVAR ======
    def salvar(self):
        dados = self.validar()
        if not dados:
            return

        nome, preco, qtd = dados

        produto = {
            "nome": nome,
            "categoria": self.categoria.get(),
            "preco": preco,
            "quantidade": qtd,
            "descricao": self.desc_text.get("1.0", tk.END).strip()
        }

        banco_produtos.append(produto)

        self.feedback.config(text="✔ Produto cadastrado com sucesso!", fg="green")
        self.limpar()

    # ====== LIMPAR ======
    def limpar(self):
        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.qtd_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.categoria.current(0)
        self.feedback.config(text="")

    # ====== VOLTAR ======
    def voltar(self):
        self.root.destroy()


# ====== EXECUÇÃO ======
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaCadastro(root)
    root.mainloop()