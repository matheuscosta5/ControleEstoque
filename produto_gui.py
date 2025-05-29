import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

class ProdutoForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Produto")
        self.geometry("650x550")
        self.grab_set()

        self.label_title = ctk.CTkLabel(self, text="Produto", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # ID
        self.label_id = ctk.CTkLabel(self, text="ID:")
        self.label_id.pack()
        self.entry_id = ctk.CTkEntry(self)
        self.entry_id.pack()

        # Nome
        self.label_nome = ctk.CTkLabel(self, text="Nome:")
        self.label_nome.pack()
        self.entry_nome = ctk.CTkEntry(self)
        self.entry_nome.pack()

        # Código de Barras
        self.label_codigo_barras = ctk.CTkLabel(self, text="Código de Barras:")
        self.label_codigo_barras.pack()
        self.entry_codigo_barras = ctk.CTkEntry(self)
        self.entry_codigo_barras.pack()

        # Descrição
        self.label_descricao = ctk.CTkLabel(self, text="Descrição:")
        self.label_descricao.pack()
        self.entry_descricao = ctk.CTkEntry(self)
        self.entry_descricao.pack()

        # Preço
        self.label_preco = ctk.CTkLabel(self, text="Preço:")
        self.label_preco.pack()
        self.entry_preco = ctk.CTkEntry(self)
        self.entry_preco.pack()

        # Quantidade em Estoque
        self.label_qtd_estoque = ctk.CTkLabel(self, text="Quantidade em Estoque:")
        self.label_qtd_estoque.pack()
        self.entry_qtd_estoque = ctk.CTkEntry(self)
        self.entry_qtd_estoque.pack()

        # Fornecedor (ID)
        self.label_fornecedor_id = ctk.CTkLabel(self, text="Fornecedor ID:")
        self.label_fornecedor_id.pack()
        self.entry_fornecedor_id = ctk.CTkEntry(self)
        self.entry_fornecedor_id.pack()

        # Botões
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=15)

        self.btn_salvar = ctk.CTkButton(self.btn_frame, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=0, column=0, padx=10)

        self.btn_buscar = ctk.CTkButton(self.btn_frame, text="Buscar", command=self.buscar)
        self.btn_buscar.grid(row=0, column=1, padx=10)

        self.btn_deletar = ctk.CTkButton(self.btn_frame, text="Deletar", command=self.deletar)
        self.btn_deletar.grid(row=0, column=2, padx=10)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=3, padx=10)

    def conectar_bd(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="controleestoque"
        )

    def salvar(self):
        id_produto = self.entry_id.get().strip()
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

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            if id_produto == "":
                sql = """INSERT INTO produto (Nome, CodigoBarras, Descricao, Preco, QuantidadeEstoque, FornecedorId) 
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                valores = (nome, codigo_barras, descricao, preco_float, qtd_estoque_int, fornecedor_id)
                cursor.execute(sql, valores)
                conexao.commit()
                messagebox.showinfo("Sucesso", "Produto inserido com sucesso!")
            else:
                sql = """UPDATE produto 
                         SET Nome=%s, CodigoBarras=%s, Descricao=%s, Preco=%s, QuantidadeEstoque=%s, FornecedorId=%s 
                         WHERE Id=%s"""
                valores = (nome, codigo_barras, descricao, preco_float, qtd_estoque_int, fornecedor_id, id_produto)
                cursor.execute(sql, valores)
                conexao.commit()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

            cursor.close()
            conexao.close()
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {err}")

    def buscar(self):
        id_produto = self.entry_id.get().strip()

        if id_produto == "":
            messagebox.showwarning("Atenção", "Informe o ID para buscar!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            sql = """SELECT Id, Nome, CodigoBarras, Descricao, Preco, QuantidadeEstoque, FornecedorId 
                     FROM produto WHERE Id=%s"""
            cursor.execute(sql, (id_produto,))
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()

            if resultado:
                self.entry_id.delete(0, ctk.END)
                self.entry_id.insert(0, resultado[0])
                self.entry_nome.delete(0, ctk.END)
                self.entry_nome.insert(0, resultado[1])
                self.entry_codigo_barras.delete(0, ctk.END)
                self.entry_codigo_barras.insert(0, resultado[2])
                self.entry_descricao.delete(0, ctk.END)
                self.entry_descricao.insert(0, resultado[3])
                self.entry_preco.delete(0, ctk.END)
                self.entry_preco.insert(0, resultado[4])
                self.entry_qtd_estoque.delete(0, ctk.END)
                self.entry_qtd_estoque.insert(0, resultado[5])
                self.entry_fornecedor_id.delete(0, ctk.END)
                self.entry_fornecedor_id.insert(0, resultado[6])
            else:
                messagebox.showinfo("Buscar", "Produto não encontrado!")

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar produto: {err}")

    def deletar(self):
        id_produto = self.entry_id.get().strip()

        if id_produto == "":
            messagebox.showwarning("Atenção", "Informe o ID para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que quer deletar este produto?")
        if not confirm:
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()
            sql = "DELETE FROM produto WHERE Id=%s"
            cursor.execute(sql, (id_produto,))
            conexao.commit()
            cursor.close()
            conexao.close()
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao deletar produto: {err}")

    def limpar(self):
        self.entry_id.delete(0, ctk.END)
        self.entry_nome.delete(0, ctk.END)
        self.entry_codigo_barras.delete(0, ctk.END)
        self.entry_descricao.delete(0, ctk.END)
        self.entry_preco.delete(0, ctk.END)
        self.entry_qtd_estoque.delete(0, ctk.END)
        self.entry_fornecedor_id.delete(0, ctk.END)
