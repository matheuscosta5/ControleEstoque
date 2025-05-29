import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

class ClienteForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Cliente")
        self.geometry("700x450")
        self.grab_set()

        self.label_title = ctk.CTkLabel(self, text="Cliente", font=("Arial", 20))
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

        # CPF
        self.label_cpf = ctk.CTkLabel(self, text="CPF:")
        self.label_cpf.pack()
        self.entry_cpf = ctk.CTkEntry(self)
        self.entry_cpf.pack()

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
            password="",
            database="controleestoque"
        )

    def salvar(self):
        id_cliente = self.entry_id.get().strip()
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        print(">>> TENTANDO SALVAR CLIENTE <<<")
        print(f"ID: {id_cliente}")
        print(f"Nome: {nome}")
        print(f"CPF: {cpf}")
        print(f"Email: {email}")
        print(f"Telefone: {telefone}")
        print(f"Endereço: {endereco}")

        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            if id_cliente == "":
                sql = "INSERT INTO cliente (Nome, CPF, Email, Telefone, Endereco) VALUES (%s, %s, %s, %s, %s)"
                valores = (nome, cpf, email, telefone, endereco)
                print("SQL INSERT:", sql)
                print("VALORES:", valores)
                cursor.execute(sql, valores)
                conexao.commit()
                messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")
            else:
                sql = """UPDATE cliente SET Nome=%s, CPF=%s, Email=%s, Telefone=%s, Endereco=%s WHERE Id=%s"""
                valores = (nome, cpf, email, telefone, endereco, id_cliente)
                print("SQL UPDATE:", sql)
                print("VALORES:", valores)
                cursor.execute(sql, valores)
                conexao.commit()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

            cursor.close()
            conexao.close()
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao salvar cliente: {err}")

    def buscar(self):
        id_cliente = self.entry_id.get().strip()
        cpf = self.entry_cpf.get().strip()

        if id_cliente == "" and cpf == "":
            messagebox.showwarning("Atenção", "Informe o ID ou CPF para buscar!")
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            if id_cliente != "":
                sql = "SELECT Id, Nome, CPF, Email, Telefone, Endereco FROM cliente WHERE Id=%s"
                cursor.execute(sql, (id_cliente,))
            else:
                sql = "SELECT Id, Nome, CPF, Email, Telefone, Endereco FROM cliente WHERE CPF=%s"
                cursor.execute(sql, (cpf,))

            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()

            if resultado:
                self.entry_id.delete(0, ctk.END)
                self.entry_id.insert(0, resultado[0])
                self.entry_nome.delete(0, ctk.END)
                self.entry_nome.insert(0, resultado[1])
                self.entry_cpf.delete(0, ctk.END)
                self.entry_cpf.insert(0, resultado[2])
                self.entry_email.delete(0, ctk.END)
                self.entry_email.insert(0, resultado[3])
                self.entry_telefone.delete(0, ctk.END)
                self.entry_telefone.insert(0, resultado[4])
                self.entry_endereco.delete(0, ctk.END)
                self.entry_endereco.insert(0, resultado[5])
            else:
                messagebox.showinfo("Buscar", "Cliente não encontrado!")

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar cliente: {err}")

    def deletar(self):
        id_cliente = self.entry_id.get().strip()

        if id_cliente == "":
            messagebox.showwarning("Atenção", "Informe o ID para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que quer deletar este cliente?")
        if not confirm:
            return

        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()
            sql = "DELETE FROM cliente WHERE Id=%s"
            cursor.execute(sql, (id_cliente,))
            conexao.commit()
            cursor.close()
            conexao.close()
            messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
            self.limpar()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao deletar cliente: {err}")

    def limpar(self):
        self.entry_id.delete(0, ctk.END)
        self.entry_nome.delete(0, ctk.END)
        self.entry_cpf.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)
