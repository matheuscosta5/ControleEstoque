import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from Conexao import Conexao

class ClienteForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Cliente")
        self.geometry("900x500")
        self.grab_set()
        self.db = Conexao()  # Instancia a conexão

        self.label_title = ctk.CTkLabel(self, text="Cliente", font=("Arial", 20))
        self.label_title.pack(pady=10)

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

        self.btn_atualizar = ctk.CTkButton(self.btn_frame, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.grid(row=0, column=1, padx=10)

        self.btn_buscar = ctk.CTkButton(self.btn_frame, text="Buscar", command=self.buscar)
        self.btn_buscar.grid(row=0, column=2, padx=10)

        self.btn_deletar = ctk.CTkButton(self.btn_frame, text="Deletar", command=self.deletar)
        self.btn_deletar.grid(row=0, column=3, padx=10)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=4, padx=10)


        # Título da tabela de clientes
        self.label_tabela_clientes = ctk.CTkLabel(self, text="Clientes cadastrados", font=("Arial", 14, "bold"))
        self.label_tabela_clientes.pack(pady=(0, 2))

        # Tabela de clientes
        self.tree = ttk.Treeview(self, columns=("Nome", "CPF", "Email", "Telefone", "Endereco"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("CPF", text="CPF")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Endereco", text="Endereço")
        self.tree.pack(pady=10, fill="x")

        self.tree.bind("<Double-1>", self.on_tree_select)

        self.atualizar_tabela_clientes()

    def atualizar_tabela_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for cliente in self.db.buscar_clientes():
            self.tree.insert("", "end", values=(
                cliente["Nome"], cliente["CPF"], cliente["Email"], cliente["Telefone"], cliente["Endereco"]
            ))

    def on_tree_select(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.entry_nome.delete(0, ctk.END)
        self.entry_nome.insert(0, valores[0])
        self.entry_cpf.delete(0, ctk.END)
        self.entry_cpf.insert(0, valores[1])
        self.entry_email.delete(0, ctk.END)
        self.entry_email.insert(0, valores[2])
        self.entry_telefone.delete(0, ctk.END)
        self.entry_telefone.insert(0, valores[3])
        self.entry_endereco.delete(0, ctk.END)
        self.entry_endereco.insert(0, valores[4])

        # Oculta o botão Salvar para evitar duplicidade
        self.btn_salvar.grid_remove()

    def salvar(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios!")
            return

        # Verifica se já existe cliente com esse CPF
        clientes = self.db.buscar_clientes()
        cliente = next((c for c in clientes if c["CPF"] == cpf), None)

        if cliente is None:
            sucesso = self.db.inserir_cliente(nome, cpf, email, telefone, endereco)
            if sucesso:
                messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")
                self.limpar()
            else:
                messagebox.showerror("Erro", "Erro ao inserir cliente.")
        else:
            # Atualizar cliente existente
            try:
                conn = self.db.conectar()
                cursor = conn.cursor()
                sql = "UPDATE Cliente SET Nome=%s, Email=%s, Telefone=%s, Endereco=%s WHERE CPF=%s"
                cursor.execute(sql, (nome, email, telefone, endereco, cpf))
                conn.commit()
                cursor.close()
                self.db.desconectar()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                self.limpar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")

        self.atualizar_tabela_clientes()

    def buscar(self):
        cpf = self.entry_cpf.get().strip()
        if cpf == "":
            messagebox.showwarning("Atenção", "Informe o CPF para buscar!")
            return

        clientes = self.db.buscar_clientes()
        cliente = next((c for c in clientes if c["CPF"] == cpf), None)
        if cliente:
            self.entry_nome.delete(0, ctk.END)
            self.entry_nome.insert(0, cliente["Nome"])
            self.entry_cpf.delete(0, ctk.END)
            self.entry_cpf.insert(0, cliente["CPF"])
            self.entry_email.delete(0, ctk.END)
            self.entry_email.insert(0, cliente["Email"])
            self.entry_telefone.delete(0, ctk.END)
            self.entry_telefone.insert(0, cliente["Telefone"])
            self.entry_endereco.delete(0, ctk.END)
            self.entry_endereco.insert(0, cliente["Endereco"])
        else:
            messagebox.showinfo("Buscar", "Cliente não encontrado!")

    def deletar(self):
        cpf = self.entry_cpf.get().strip()
        if cpf == "":
            messagebox.showwarning("Atenção", "Informe o CPF para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que quer deletar este cliente?")
        if not confirm:
            return

        # Busca o cliente pelo CPF para pegar o ID
        clientes = self.db.buscar_clientes()
        cliente = next((c for c in clientes if c["CPF"] == cpf), None)
        if cliente:
            sucesso = self.db.deletar_cliente(cliente["Id"])
            if sucesso:
                messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
                self.limpar()
            else:
                messagebox.showerror("Erro", "Erro ao deletar cliente.")
        else:
            messagebox.showinfo("Buscar", "Cliente não encontrado!")

        self.atualizar_tabela_clientes()

    def limpar(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_cpf.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)
        # Exibe novamente o botão Salvar
        self.btn_salvar.grid()
        # Atualiza a tabela se necessário
        self.atualizar_tabela_clientes()

    def atualizar(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome or not cpf:
            messagebox.showwarning("Atenção", "Nome e CPF são obrigatórios!")
            return

        clientes = self.db.buscar_clientes()
        cliente = next((c for c in clientes if c["CPF"] == cpf), None)

        if cliente:
            sucesso = self.db.atualizar_cliente(cliente["Id"], nome, cpf, email, telefone, endereco)
            if sucesso:
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                self.limpar()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar cliente.")
        else:
            messagebox.showinfo("Atualizar", "Cliente não encontrado para atualizar.")

        self.atualizar_tabela_clientes()
