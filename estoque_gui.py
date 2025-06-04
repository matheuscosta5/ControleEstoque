import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from Conexao import Conexao

class EstoqueForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Estoque")
        self.geometry("1050x750")
        self.grab_set()
        self.db = Conexao()

        self.label_title = ctk.CTkLabel(self, text="Movimentação de Estoque", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Frame horizontal principal
        main_row = ctk.CTkFrame(self)
        main_row.pack(pady=5, fill="both", expand=True)

        # Coluna de campos (à esquerda)
        campos_col = ctk.CTkFrame(main_row)
        campos_col.pack(side="left", fill="y", expand=True, padx=(0, 10))

        # Campo ID para busca/atualização
        self.label_id = ctk.CTkLabel(campos_col, text="ID da Movimentação (para buscar/atualizar):")
        self.label_id.pack()
        self.entry_id = ctk.CTkEntry(campos_col)
        self.entry_id.pack()

        # Tipo de Movimentação
        self.label_tipo = ctk.CTkLabel(campos_col, text="Tipo de Movimentação:")
        self.label_tipo.pack()
        self.combo_tipo = ctk.CTkComboBox(campos_col, values=["ENTRADA", "SAIDA"])
        self.combo_tipo.pack()

        # Quantidade
        self.label_quantidade = ctk.CTkLabel(campos_col, text="Quantidade:")
        self.label_quantidade.pack()
        self.entry_quantidade = ctk.CTkEntry(campos_col)
        self.entry_quantidade.pack()

        # Produto ID
        self.label_produto_id = ctk.CTkLabel(campos_col, text="Produto ID:")
        self.label_produto_id.pack()
        self.entry_produto_id = ctk.CTkEntry(campos_col)
        self.entry_produto_id.pack()

        # Fornecedor ID
        self.label_fornecedor_id = ctk.CTkLabel(campos_col, text="Fornecedor ID:")
        self.label_fornecedor_id.pack()
        self.entry_fornecedor_id = ctk.CTkEntry(campos_col)
        self.entry_fornecedor_id.pack()

        # Cliente ID
        self.label_cliente_id = ctk.CTkLabel(campos_col, text="Cliente ID:")
        self.label_cliente_id.pack()
        self.entry_cliente_id = ctk.CTkEntry(campos_col)
        self.entry_cliente_id.pack()

        # Observação
        self.label_obs = ctk.CTkLabel(campos_col, text="Observação:")
        self.label_obs.pack()
        self.entry_obs = ctk.CTkEntry(campos_col)
        self.entry_obs.pack()

        # Botões
        self.btn_frame = ctk.CTkFrame(campos_col)
        self.btn_frame.pack(pady=15)

        self.btn_salvar = ctk.CTkButton(self.btn_frame, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=0, column=0, padx=10)

        self.btn_atualizar = ctk.CTkButton(self.btn_frame, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.grid(row=0, column=1, padx=10)

        self.btn_buscar = ctk.CTkButton(self.btn_frame, text="Buscar", command=self.buscar)
        self.btn_buscar.grid(row=0, column=2, padx=10)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=3, padx=10)

        # Coluna das tabelas auxiliares (à direita)
        tabelas_col = ctk.CTkFrame(main_row)
        tabelas_col.pack(side="left", fill="both", expand=True)

        # Tabela de Produtos (primeira)
        self.label_tabela_produtos = ctk.CTkLabel(tabelas_col, text="Produtos", font=("Arial", 14, "bold"))
        self.label_tabela_produtos.pack(pady=(0, 2))
        self.tree_produtos = ttk.Treeview(tabelas_col, columns=("Id", "Nome"), show="headings", height=5)
        self.tree_produtos.heading("Id", text="ID")
        self.tree_produtos.heading("Nome", text="Nome")
        self.tree_produtos.column("Id", width=40, anchor="center")
        self.tree_produtos.column("Nome", width=120)
        self.tree_produtos.pack(padx=5, pady=5, fill="x")
        self.atualizar_tabela_produtos()

        # Tabela de Fornecedores (segunda)
        self.label_tabela_fornecedores = ctk.CTkLabel(tabelas_col, text="Fornecedores", font=("Arial", 14, "bold"))
        self.label_tabela_fornecedores.pack(pady=(10, 2))
        self.tree_fornecedores = ttk.Treeview(tabelas_col, columns=("Id", "RazaoSocial"), show="headings", height=5)
        self.tree_fornecedores.heading("Id", text="ID")
        self.tree_fornecedores.heading("RazaoSocial", text="Nome")
        self.tree_fornecedores.column("Id", width=40, anchor="center")
        self.tree_fornecedores.column("RazaoSocial", width=120)
        self.tree_fornecedores.pack(padx=5, pady=5, fill="x")
        self.atualizar_tabela_fornecedores()

        # Tabela de Clientes (terceira)
        self.label_tabela_clientes = ctk.CTkLabel(tabelas_col, text="Clientes", font=("Arial", 14, "bold"))
        self.label_tabela_clientes.pack(pady=(10, 2))
        self.tree_clientes = ttk.Treeview(tabelas_col, columns=("Id", "Nome"), show="headings", height=5)
        self.tree_clientes.heading("Id", text="ID")
        self.tree_clientes.heading("Nome", text="Nome")
        self.tree_clientes.column("Id", width=40, anchor="center")
        self.tree_clientes.column("Nome", width=120)
        self.tree_clientes.pack(padx=5, pady=5, fill="x")
        self.atualizar_tabela_clientes()

        # Título da tabela de estoque
        self.label_tabela_estoque = ctk.CTkLabel(self, text="Movimentações de Estoque", font=("Arial", 14, "bold"))
        self.label_tabela_estoque.pack(pady=(10, 2))

        # Tabela de Estoque
        self.tree_estoque = ttk.Treeview(self, columns=("Id", "TipoMovimentacao", "Quantidade", "ProdutoId", "FornecedorId", "ClienteId", "Observacao"), show="headings")
        self.tree_estoque.heading("Id", text="ID")
        self.tree_estoque.heading("TipoMovimentacao", text="Tipo")
        self.tree_estoque.heading("Quantidade", text="Quantidade")
        self.tree_estoque.heading("ProdutoId", text="Produto ID")
        self.tree_estoque.heading("FornecedorId", text="Fornecedor ID")
        self.tree_estoque.heading("ClienteId", text="Cliente ID")
        self.tree_estoque.heading("Observacao", text="Observação")
        self.tree_estoque.pack(pady=10, fill="x")
        self.atualizar_tabela_estoque()

        # Vincula o evento de seleção da árvore de estoque
        self.tree_estoque.bind("<Double-1>", self.on_tree_estoque_select)
        self.tree_clientes.bind("<Double-1>", self.on_tree_cliente_select)
        self.tree_fornecedores.bind("<Double-1>", self.on_tree_fornecedor_select)
        self.tree_produtos.bind("<Double-1>", self.on_tree_produto_select)

    def atualizar_tabela_estoque(self):
        for row in self.tree_estoque.get_children():
            self.tree_estoque.delete(row)
        for mov in self.db.buscar_estoque():
            self.tree_estoque.insert("", "end", values=(
                mov["Id"], mov["TipoMovimentacao"], mov["Quantidade"], mov["ProdutoId"],
                mov["FornecedorId"], mov["ClienteId"], mov["Observacao"]
            ))

    def atualizar_tabela_clientes(self):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)
        for cliente in self.db.buscar_clientes():
            self.tree_clientes.insert("", "end", values=(cliente["Id"], cliente["Nome"]))

    def atualizar_tabela_fornecedores(self):
        for row in self.tree_fornecedores.get_children():
            self.tree_fornecedores.delete(row)
        for fornecedor in self.db.buscar_fornecedores():
            self.tree_fornecedores.insert("", "end", values=(fornecedor["Id"], fornecedor["RazaoSocial"]))

    def atualizar_tabela_produtos(self):
        for row in self.tree_produtos.get_children():
            self.tree_produtos.delete(row)
        for produto in self.db.buscar_produtos():
            self.tree_produtos.insert("", "end", values=(produto["Id"], produto["Nome"]))

    def salvar(self):
        tipo = self.combo_tipo.get()
        quantidade = self.entry_quantidade.get().strip()
        produto_id = self.entry_produto_id.get().strip()
        fornecedor_id = self.entry_fornecedor_id.get().strip()
        cliente_id = self.entry_cliente_id.get().strip()
        observacao = self.entry_obs.get().strip()

        if not tipo or not quantidade or not produto_id:
            messagebox.showwarning("Atenção", "Tipo, Quantidade e Produto ID são obrigatórios!")
            return

        try:
            quantidade_int = int(quantidade)
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidade deve ser um número inteiro!")
            return

        sucesso = self.db.inserir_estoque(tipo, quantidade_int, produto_id, fornecedor_id, cliente_id, observacao)
        if sucesso:
            messagebox.showinfo("Sucesso", "Movimentação inserida com sucesso!")
            self.limpar()
        else:
            messagebox.showerror("Erro", "Erro ao inserir movimentação.")

        self.atualizar_tabela_estoque()

    def buscar(self):
        id_mov = self.entry_id.get().strip()
        if not id_mov:
            messagebox.showwarning("Atenção", "Informe o ID da movimentação para buscar!")
            return

        movimentos = self.db.buscar_estoque(apenas_ativos=False)
        mov = next((m for m in movimentos if str(m["Id"]) == id_mov), None)

        if mov:
            self.combo_tipo.set(mov["TipoMovimentacao"])
            self.entry_quantidade.delete(0, ctk.END)
            self.entry_quantidade.insert(0, mov["Quantidade"])
            self.entry_produto_id.delete(0, ctk.END)
            self.entry_produto_id.insert(0, mov["ProdutoId"])
            self.entry_fornecedor_id.delete(0, ctk.END)
            self.entry_fornecedor_id.insert(0, mov["FornecedorId"])
            self.entry_cliente_id.delete(0, ctk.END)
            self.entry_cliente_id.insert(0, mov["ClienteId"])
            self.entry_obs.delete(0, ctk.END)
            self.entry_obs.insert(0, mov["Observacao"])
        else:
            messagebox.showinfo("Buscar", "Movimentação não encontrada!")

    def atualizar(self):
        id_mov = self.entry_id.get().strip()
        tipo = self.combo_tipo.get()
        quantidade = self.entry_quantidade.get().strip()
        produto_id = self.entry_produto_id.get().strip()
        fornecedor_id = self.entry_fornecedor_id.get().strip()
        cliente_id = self.entry_cliente_id.get().strip()
        observacao = self.entry_obs.get().strip()

        if not id_mov:
            messagebox.showwarning("Atenção", "Informe o ID da movimentação para atualizar!")
            return

        if not tipo or not quantidade or not produto_id:
            messagebox.showwarning("Atenção", "Tipo, Quantidade e Produto ID são obrigatórios!")
            return

        try:
            quantidade_int = int(quantidade)
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidade deve ser um número inteiro!")
            return

        sucesso = self.db.atualizar_estoque(id_mov, tipo, quantidade_int, produto_id, fornecedor_id, cliente_id, observacao)
        if sucesso:
            messagebox.showinfo("Sucesso", "Movimentação atualizada com sucesso!")
            self.limpar()
        else:
            messagebox.showerror("Erro", "Erro ao atualizar movimentação.")

        self.atualizar_tabela_estoque()

    def limpar(self):
        self.entry_id.delete(0, ctk.END)
        self.combo_tipo.set("")
        self.entry_quantidade.delete(0, ctk.END)
        self.entry_produto_id.delete(0, ctk.END)
        self.entry_fornecedor_id.delete(0, ctk.END)
        self.entry_cliente_id.delete(0, ctk.END)
        self.entry_obs.delete(0, ctk.END)
        self.atualizar_tabela_estoque()

    def on_tree_estoque_select(self, event):
        item = self.tree_estoque.selection()[0]
        valores = self.tree_estoque.item(item, "values")
        # Preenche os campos com os valores da linha selecionada
        self.entry_id.delete(0, ctk.END)
        self.entry_id.insert(0, valores[0])
        self.combo_tipo.set(valores[1])
        self.entry_quantidade.delete(0, ctk.END)
        self.entry_quantidade.insert(0, valores[2])
        self.entry_produto_id.delete(0, ctk.END)
        self.entry_produto_id.insert(0, valores[3])
        self.entry_fornecedor_id.delete(0, ctk.END)
        self.entry_fornecedor_id.insert(0, valores[4])
        self.entry_cliente_id.delete(0, ctk.END)
        self.entry_cliente_id.insert(0, valores[5])
        self.entry_obs.delete(0, ctk.END)
        self.entry_obs.insert(0, valores[6])

    def on_tree_cliente_select(self, event):
        item = self.tree_clientes.selection()[0]
        valores = self.tree_clientes.item(item, "values")
        self.entry_cliente_id.delete(0, ctk.END)
        self.entry_cliente_id.insert(0, valores[0])

    def on_tree_fornecedor_select(self, event):
        item = self.tree_fornecedores.selection()[0]
        valores = self.tree_fornecedores.item(item, "values")
        self.entry_fornecedor_id.delete(0, ctk.END)
        self.entry_fornecedor_id.insert(0, valores[0])

    def on_tree_produto_select(self, event):
        item = self.tree_produtos.selection()[0]
        valores = self.tree_produtos.item(item, "values")
        self.entry_produto_id.delete(0, ctk.END)
        self.entry_produto_id.insert(0, valores[0])
