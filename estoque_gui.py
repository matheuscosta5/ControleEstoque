import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

class EstoqueForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Controle de Estoque")
        self.geometry("700x630")
        self.grab_set()

        self.label_title = ctk.CTkLabel(self, text="Estoque", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # ID
        self.label_id = ctk.CTkLabel(self, text="ID:")
        self.label_id.pack()
        self.entry_id = ctk.CTkEntry(self)
        self.entry_id.pack()

        # Tipo Movimentação
        self.label_tipo = ctk.CTkLabel(self, text="Tipo Movimentação:")
        self.label_tipo.pack()
        self.entry_tipo = ctk.CTkEntry(self)
        self.entry_tipo.pack()

        # Quantidade
        self.label_quantidade = ctk.CTkLabel(self, text="Quantidade:")
        self.label_quantidade.pack()
        self.entry_quantidade = ctk.CTkEntry(self)
        self.entry_quantidade.pack()

        # Data Movimentação
        self.label_data = ctk.CTkLabel(self, text="Data Movimentação:")
        self.label_data.pack()
        self.entry_data = ctk.CTkEntry(self)
        self.entry_data.pack()

        # Ativo
        self.label_ativo = ctk.CTkLabel(self, text="Ativo (1 ou 0):")
        self.label_ativo.pack()
        self.entry_ativo = ctk.CTkEntry(self)
        self.entry_ativo.pack()

        # Observação
        self.label_obs = ctk.CTkLabel(self, text="Observação:")
        self.label_obs.pack()
        self.entry_obs = ctk.CTkEntry(self)
        self.entry_obs.pack()

        # Cliente ID
        self.label_cliente = ctk.CTkLabel(self, text="Cliente ID:")
        self.label_cliente.pack()
        self.entry_cliente = ctk.CTkEntry(self)
        self.entry_cliente.pack()

        # Fornecedor ID
        self.label_fornecedor = ctk.CTkLabel(self, text="Fornecedor ID:")
        self.label_fornecedor.pack()
        self.entry_fornecedor = ctk.CTkEntry(self)
        self.entry_fornecedor.pack()

        # Produto ID
        self.label_produto = ctk.CTkLabel(self, text="Produto ID:")
        self.label_produto.pack()
        self.entry_produto = ctk.CTkEntry(self)
        self.entry_produto.pack()

        # Botões
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=15)

        self.btn_salvar = ctk.CTkButton(self.btn_frame, text="Salvar", command=self.salvar)
        self.btn_salvar.grid(row=0, column=0, padx=5)

        self.btn_buscar = ctk.CTkButton(self.btn_frame, text="Buscar", command=self.buscar)
        self.btn_buscar.grid(row=0, column=1, padx=5)

        self.btn_deletar = ctk.CTkButton(self.btn_frame, text="Deletar", command=self.deletar)
        self.btn_deletar.grid(row=0, column=2, padx=5)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=3, padx=5)

    def conectar_bd(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="controleestoque"
        )

    def salvar(self):
        dados = {
            "id": self.entry_id.get().strip(),
            "tipo": self.entry_tipo.get().strip(),
            "quantidade": self.entry_quantidade.get().strip(),
            "data": self.entry_data.get().strip(),
            "ativo": self.entry_ativo.get().strip(),
            "obs": self.entry_obs.get().strip(),
            "cliente": self.entry_cliente.get().strip(),
            "fornecedor": self.entry_fornecedor.get().strip(),
            "produto": self.entry_produto.get().strip()
        }

        if not dados["quantidade"] or not dados["produto"]:
            messagebox.showwarning("Atenção", "Produto ID e Quantidade são obrigatórios!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            if dados["id"] == "":
                sql = """INSERT INTO estoque 
                         (TipoMovimentacao, Quantidade, DataMovimentacao, Ativo, Observacao, ClienteId, FornecedorId, ProdutoId) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (
                    dados["tipo"], dados["quantidade"], dados["data"], dados["ativo"],
                    dados["obs"], dados["cliente"], dados["fornecedor"], dados["produto"]
                )
                cursor.execute(sql, valores)
                messagebox.showinfo("Sucesso", "Registro inserido com sucesso!")
            else:
                sql = """UPDATE estoque SET 
                            TipoMovimentacao=%s, Quantidade=%s, DataMovimentacao=%s,
                            Ativo=%s, Observacao=%s, ClienteId=%s, FornecedorId=%s, ProdutoId=%s 
                         WHERE Id=%s"""
                valores = (
                    dados["tipo"], dados["quantidade"], dados["data"], dados["ativo"],
                    dados["obs"], dados["cliente"], dados["fornecedor"], dados["produto"],
                    dados["id"]
                )
                cursor.execute(sql, valores)
                messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")

            conexao.commit()
            cursor.close()
            conexao.close()
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao salvar: {err}")

    def buscar(self):
        id_estoque = self.entry_id.get().strip()

        if not id_estoque:
            messagebox.showwarning("Atenção", "Informe o ID para buscar!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM estoque WHERE Id=%s", (id_estoque,))
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()

            if resultado:
                campos = [
                    self.entry_id, self.entry_tipo, self.entry_quantidade,
                    self.entry_data, self.entry_ativo, self.entry_obs,
                    self.entry_cliente, self.entry_fornecedor, self.entry_produto
                ]
                for i, campo in enumerate(campos):
                    campo.delete(0, ctk.END)
                    campo.insert(0, str(resultado[i]))
            else:
                messagebox.showinfo("Buscar", "Registro não encontrado.")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar: {err}")

    def deletar(self):
        id_estoque = self.entry_id.get().strip()

        if not id_estoque:
            messagebox.showwarning("Atenção", "Informe o ID para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Deseja deletar este registro?")
        if not confirm:
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM estoque WHERE Id=%s", (id_estoque,))
            conexao.commit()
            cursor.close()
            conexao.close()
            messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao deletar: {err}")

    def limpar(self):
        entradas = [
            self.entry_id, self.entry_tipo, self.entry_quantidade, self.entry_data,
            self.entry_ativo, self.entry_obs, self.entry_cliente, self.entry_fornecedor,
            self.entry_produto
        ]
        for entrada in entradas:
            entrada.delete(0, ctk.END)
