import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from Conexao import Conexao

class ProdutoForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Produto")
        self.geometry("900x600")
        self.grab_set()
        self.db = Conexao()

        self.label_title = ctk.CTkLabel(self, text="Produto", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Frame horizontal para campos e tabela de fornecedores
        main_row = ctk.CTkFrame(self)
        main_row.pack(pady=5, fill="x", expand=True)

        # Frame da coluna de campos (à esquerda)
        campos_col = ctk.CTkFrame(main_row)
        campos_col.pack(side="left", fill="y", expand=True, padx=(0, 10))

        # Nome
        self.label_nome = ctk.CTkLabel(campos_col, text="Nome:")
        self.label_nome.pack()
        self.entry_nome = ctk.CTkEntry(campos_col)
        self.entry_nome.pack()

        # Código de Barras
        self.label_codigo_barras = ctk.CTkLabel(campos_col, text="Código de Barras:")
        self.label_codigo_barras.pack()
        self.entry_codigo_barras = ctk.CTkEntry(campos_col)
        self.entry_codigo_barras.pack()

        # Descrição
        self.label_descricao = ctk.CTkLabel(campos_col, text="Descrição:")
        self.label_descricao.pack()
        self.entry_descricao = ctk.CTkEntry(campos_col)
        self.entry_descricao.pack()

        # Preço
        self.label_preco = ctk.CTkLabel(campos_col, text="Preço:")
        self.label_preco.pack()
        self.entry_preco = ctk.CTkEntry(campos_col)
        self.entry_preco.pack()

        # Quantidade em Estoque
        self.label_qtd_estoque = ctk.CTkLabel(campos_col, text="Quantidade em Estoque:")
        self.label_qtd_estoque.pack()
        self.entry_qtd_estoque = ctk.CTkEntry(campos_col)
        self.entry_qtd_estoque.pack()

        # Fornecedor ID (embaixo dos outros campos)
        self.label_fornecedor_id = ctk.CTkLabel(campos_col, text="Fornecedor ID:")
        self.label_fornecedor_id.pack()
        self.entry_fornecedor_id = ctk.CTkEntry(campos_col, width=80)
        self.entry_fornecedor_id.pack(pady=(0, 5))

        # Frame da coluna da tabela (à direita)
        tabela_col = ctk.CTkFrame(main_row)
        tabela_col.pack(side="left", fill="y")

        # Título da tabela de fornecedores
        self.label_tabela_fornecedores = ctk.CTkLabel(tabela_col, text="Fornecedores cadastrados", font=("Arial", 14, "bold"))
        self.label_tabela_fornecedores.pack(pady=(0, 2))

        self.tree_fornecedores = ttk.Treeview(tabela_col, columns=("Id", "RazaoSocial"), show="headings", height=10)
        self.tree_fornecedores.heading("Id", text="ID")
        self.tree_fornecedores.heading("RazaoSocial", text="Nome")
        self.tree_fornecedores.column("Id", width=40, anchor="center")
        self.tree_fornecedores.column("RazaoSocial", width=120)
        self.tree_fornecedores.pack(padx=5, pady=5, fill="y")

        self.tree_fornecedores.bind("<Double-1>", self.on_fornecedor_select)

        self.atualizar_tabela_fornecedores()

        # Botões
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=15)

        self.btn_salvar = ctk.CTkButton(self.btn_frame, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=0, column=0, padx=10)

        self.btn_atualizar = ctk.CTkButton(self.btn_frame, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.grid(row=0, column=1, padx=10)

        self.btn_buscar = ctk.CTkButton(self.btn_frame, text="Buscar", command=self.buscar)
        self.btn_buscar.grid(row=0, column=2, padx=10)

        self.btn_deletar = ctk.CTkButton(self.btn_frame, text="Deletar", command=self.deletar)
        self.btn_deletar.grid(row=0, column=3, padx=10)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=4, padx=10)

        # Título da tabela de produtos
        self.label_tabela_produtos = ctk.CTkLabel(self, text="Produtos cadastrados", font=("Arial", 14, "bold"))
        self.label_tabela_produtos.pack(pady=(0, 2))

        # Tabela de produtos
        self.tree = ttk.Treeview(self, columns=("Nome", "CodigoBarras", "Descricao", "Preco", "QuantidadeEstoque", "FornecedorPadraoId"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CodigoBarras", text="Código de Barras")
        self.tree.heading("Descricao", text="Descrição")
        self.tree.heading("Preco", text="Preço")
        self.tree.heading("QuantidadeEstoque", text="Qtd. Estoque")
        self.tree.heading("FornecedorPadraoId", text="Fornecedor ID")
        self.tree.pack(pady=10, fill="x")

        self.tree.bind("<Double-1>", self.on_tree_select)

        self.atualizar_tabela_produtos()

    def atualizar_tabela_produtos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for produto in self.db.buscar_produtos():
            self.tree.insert("", "end", values=(
                produto["Nome"], produto["CodigoBarras"], produto["Descricao"],
                produto["Preco"], produto["QuantidadeEstoque"], produto["FornecedorPadraoId"]
            ))

    def on_tree_select(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.entry_nome.delete(0, ctk.END)
        self.entry_nome.insert(0, valores[0])
        self.entry_codigo_barras.delete(0, ctk.END)
        self.entry_codigo_barras.insert(0, valores[1])
        self.entry_descricao.delete(0, ctk.END)
        self.entry_descricao.insert(0, valores[2])
        self.entry_preco.delete(0, ctk.END)
        self.entry_preco.insert(0, valores[3])
        self.entry_qtd_estoque.delete(0, ctk.END)
        self.entry_qtd_estoque.insert(0, valores[4])
        self.entry_fornecedor_id.delete(0, ctk.END)
        self.entry_fornecedor_id.insert(0, valores[5])
        self.btn_salvar.grid_remove()

    def atualizar_tabela_fornecedores(self):
        for row in self.tree_fornecedores.get_children():
            self.tree_fornecedores.delete(row)
        for fornecedor in self.db.buscar_fornecedores():
            self.tree_fornecedores.insert("", "end", values=(fornecedor["Id"], fornecedor["RazaoSocial"]))

    def on_fornecedor_select(self, event):
        item = self.tree_fornecedores.selection()[0]
        valores = self.tree_fornecedores.item(item, "values")
        self.entry_fornecedor_id.delete(0, ctk.END)
        self.entry_fornecedor_id.insert(0, valores[0])

    def salvar(self):
        nome = self.entry_nome.get().strip()
        codigo_barras = self.entry_codigo_barras.get().strip()
        descricao = self.entry_descricao.get().strip()
        preco = self.entry_preco.get().strip()
        qtd_estoque = self.entry_qtd_estoque.get().strip()
        fornecedor_id = self.entry_fornecedor_id.get().strip()

        if not nome or not preco or not fornecedor_id:
            messagebox.showwarning("Atenção", "Nome, Preço e Fornecedor ID são obrigatórios!")
            return

        try:
            preco_float = float(preco)
            qtd_estoque_int = int(qtd_estoque) if qtd_estoque else 0
        except ValueError:
            messagebox.showwarning("Atenção", "Preço e Quantidade devem ser valores numéricos válidos!")
            return

        sucesso = self.db.inserir_produto(
            nome, codigo_barras, preco_float, qtd_estoque_int, descricao, fornecedor_id
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")
            self.limpar()
        else:
            messagebox.showerror("Erro", "Erro ao inserir produto.")

        self.atualizar_tabela_produtos()

    def atualizar(self):
        # Para atualizar, você precisa buscar o produto pelo nome/código de barras ou outro identificador único
        # Aqui está um exemplo usando nome e código de barras (ajuste conforme sua lógica)
        nome = self.entry_nome.get().strip()
        codigo_barras = self.entry_codigo_barras.get().strip()
        descricao = self.entry_descricao.get().strip()
        preco = self.entry_preco.get().strip()
        qtd_estoque = self.entry_qtd_estoque.get().strip()
        fornecedor_id = self.entry_fornecedor_id.get().strip()

        if not nome or not preco or not fornecedor_id:
            messagebox.showwarning("Atenção", "Nome, Preço e Fornecedor ID são obrigatórios!")
            return

        try:
            preco_float = float(preco)
            qtd_estoque_int = int(qtd_estoque) if qtd_estoque else 0
        except ValueError:
            messagebox.showwarning("Atenção", "Preço e Quantidade devem ser valores numéricos válidos!")
            return

        # Busque o produto para pegar o ID
        produtos = self.db.buscar_produtos()
        produto = next((p for p in produtos if p["Nome"] == nome and p["CodigoBarras"] == codigo_barras), None)
        if not produto:
            messagebox.showwarning("Atenção", "Selecione um produto válido para atualizar!")
            return

        sucesso = self.db.atualizar_produto(
            produto["Id"], nome, codigo_barras, preco_float, qtd_estoque_int, descricao, fornecedor_id
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.limpar()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar produto.")

        self.atualizar_tabela_produtos()

    def buscar(self):
        codigo_barras = self.entry_codigo_barras.get().strip()

        if not codigo_barras:
            messagebox.showwarning("Atenção", "Informe o Código de Barras para buscar!")
            return

        produtos = self.db.buscar_produtos()
        produto = next((p for p in produtos if p["CodigoBarras"] == codigo_barras), None)

        if produto:
            self.entry_nome.delete(0, ctk.END)
            self.entry_nome.insert(0, produto["Nome"])
            self.entry_codigo_barras.delete(0, ctk.END)
            self.entry_codigo_barras.insert(0, produto["CodigoBarras"])
            self.entry_descricao.delete(0, ctk.END)
            self.entry_descricao.insert(0, produto["Descricao"])
            self.entry_preco.delete(0, ctk.END)
            self.entry_preco.insert(0, produto["Preco"])
            self.entry_qtd_estoque.delete(0, ctk.END)
            self.entry_qtd_estoque.insert(0, produto["QuantidadeEstoque"])
            self.entry_fornecedor_id.delete(0, ctk.END)
            self.entry_fornecedor_id.insert(0, produto["FornecedorPadraoId"])
        else:
            messagebox.showinfo("Buscar", "Produto não encontrado!")

    def deletar(self):
        nome = self.entry_nome.get().strip()
        codigo_barras = self.entry_codigo_barras.get().strip()

        if not nome and not codigo_barras:
            messagebox.showwarning("Atenção", "Informe o Nome ou Código de Barras para deletar!")
            return

        produtos = self.db.buscar_produtos()
        produto = next((p for p in produtos if p["Nome"] == nome or p["CodigoBarras"] == codigo_barras), None)
        if not produto:
            messagebox.showwarning("Atenção", "Selecione um produto válido para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que quer deletar este produto?")
        if not confirm:
            return

        sucesso = self.db.deletar_produto(produto["Id"])
        if sucesso:
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
            self.limpar()
        else:
            messagebox.showerror("Erro", "Erro ao deletar produto.")

        self.atualizar_tabela_produtos()

    def limpar(self):
        self.btn_salvar.grid()  # Mostra novamente o botão Salvar
        self.entry_nome.delete(0, ctk.END)
        self.entry_codigo_barras.delete(0, ctk.END)
        self.entry_descricao.delete(0, ctk.END)
        self.entry_preco.delete(0, ctk.END)
        self.entry_qtd_estoque.delete(0, ctk.END)
        self.entry_fornecedor_id.delete(0, ctk.END)
        self.atualizar_tabela_produtos()
