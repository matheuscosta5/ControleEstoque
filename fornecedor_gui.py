import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

class FornecedorForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Fornecedor")
        self.geometry("700x450")
        self.grab_set()

        self.label_title = ctk.CTkLabel(self, text="Fornecedor", font=("Arial", 20))
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

        # CNPJ
        self.label_cnpj = ctk.CTkLabel(self, text="CNPJ:")
        self.label_cnpj.pack()
        self.entry_cnpj = ctk.CTkEntry(self)
        self.entry_cnpj.pack()

        # Email
        self.label_email = ctk.CTkLabel(self, text="Email:")
        self.label_email.pack()
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.pack()

        # Telefone
        self.label_telefone = ctk.CTkLabel(self, text="Telefone:")
        self.label_telefone.pack()
        self.entry_telefone = ctk.CTkEntry(self)
        self.entry_telefone.pack()

        # Endereço
        self.label_endereco = ctk.CTkLabel(self, text="Endereço:")
        self.label_endereco.pack()
        self.entry_endereco = ctk.CTkEntry(self)
        self.entry_endereco.pack()

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
            password="",  # sem senha
            database="controleestoque"
        )

    def salvar(self):
        id_fornecedor = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        cnpj = self.entry_cnpj.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome or not cnpj:
            messagebox.showwarning("Atenção", "Nome e CNPJ são obrigatórios!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            if id_fornecedor == "":
                sql = "INSERT INTO fornecedor (Nome, CNPJ, Email, Telefone, Endereco) VALUES (%s, %s, %s, %s, %s)"
                valores = (nome, cnpj, email, telefone, endereco)
                cursor.execute(sql, valores)
                conexao.commit()

                cursor.execute("SELECT LAST_INSERT_ID()")
                id_fornecedor = cursor.fetchone()[0]

                messagebox.showinfo("Sucesso", "Fornecedor inserido com sucesso!")
            else:
                sql = "UPDATE fornecedor SET Nome=%s, CNPJ=%s, Email=%s, Telefone=%s, Endereco=%s WHERE Id=%s"
                valores = (nome, cnpj, email, telefone, endereco, id_fornecedor)
                cursor.execute(sql, valores)
                conexao.commit()

                messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")

            # Impressão no console
            print(f"ID: {id_fornecedor}")
            print(f"Razão Social: {nome}")
            print(f"CNPJ: {cnpj}")
            print(f"Email: {email}")
            print(f"Telefone: {telefone}")
            print(f"Endereço: {endereco}")

            cursor.close()
            conexao.close()
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao salvar fornecedor: {err}")

    def buscar(self):
        id_fornecedor = self.entry_id.get().strip()
        cnpj = self.entry_cnpj.get().strip()

        if id_fornecedor == "" and cnpj == "":
            messagebox.showwarning("Atenção", "Informe o ID ou CNPJ para buscar!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            if id_fornecedor != "":
                sql = "SELECT Id, Nome, CNPJ, Email, Telefone, Endereco FROM fornecedor WHERE Id=%s"
                cursor.execute(sql, (id_fornecedor,))
            else:
                sql = "SELECT Id, Nome, CNPJ, Email, Telefone, Endereco FROM fornecedor WHERE CNPJ=%s"
                cursor.execute(sql, (cnpj,))

            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()

            if resultado:
                self.entry_id.delete(0, ctk.END)
                self.entry_id.insert(0, resultado[0])
                self.entry_nome.delete(0, ctk.END)
                self.entry_nome.insert(0, resultado[1])
                self.entry_cnpj.delete(0, ctk.END)
                self.entry_cnpj.insert(0, resultado[2])
                self.entry_email.delete(0, ctk.END)
                self.entry_email.insert(0, resultado[3])
                self.entry_telefone.delete(0, ctk.END)
                self.entry_telefone.insert(0, resultado[4])
                self.entry_endereco.delete(0, ctk.END)
                self.entry_endereco.insert(0, resultado[5])
            else:
                messagebox.showinfo("Buscar", "Fornecedor não encontrado!")

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar fornecedor: {err}")

    def deletar(self):
        id_fornecedor = self.entry_id.get().strip()

        if id_fornecedor == "":
            messagebox.showwarning("Atenção", "Informe o ID para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que quer deletar este fornecedor?")
        if not confirm:
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()
            sql = "DELETE FROM fornecedor WHERE Id=%s"
            cursor.execute(sql, (id_fornecedor,))
            conexao.commit()
            cursor.close()
            conexao.close()
            messagebox.showinfo("Sucesso", "Fornecedor deletado com sucesso!")
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao deletar fornecedor: {err}")

    def limpar(self):
        self.entry_id.delete(0, ctk.END)
        self.entry_nome.delete(0, ctk.END)
        self.entry_cnpj.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)
