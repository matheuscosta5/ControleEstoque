import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from Conexao import Conexao

class FornecedorForm(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Fornecedor")
        self.geometry("900x500")
        self.grab_set()
        self.db = Conexao()  # Instancia a conexão

        self.label_title = ctk.CTkLabel(self, text="Fornecedor", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Nome
        self.label_nome = ctk.CTkLabel(self, text="Razão Social:")
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

        self.btn_atualizar = ctk.CTkButton(self.btn_frame, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.grid(row=0, column=1, padx=10)

        self.btn_buscar = ctk.CTkButton(self.btn_frame, text="Buscar", command=self.buscar)
        self.btn_buscar.grid(row=0, column=2, padx=10)

        self.btn_deletar = ctk.CTkButton(self.btn_frame, text="Deletar", command=self.deletar)
        self.btn_deletar.grid(row=0, column=3, padx=10)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar)
        self.btn_limpar.grid(row=0, column=4, padx=10)

        # Título da tabela de fornecedores
        self.label_tabela_fornecedores = ctk.CTkLabel(self, text="Fornecedores cadastrados", font=("Arial", 14, "bold"))
        self.label_tabela_fornecedores.pack(pady=(0, 2))

        # Tabela de fornecedores
        self.tree = ttk.Treeview(self, columns=("RazaoSocial", "CNPJ", "Email", "Telefone", "Endereco"), show="headings")
        self.tree.heading("RazaoSocial", text="Razão Social")
        self.tree.heading("CNPJ", text="CNPJ")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Endereco", text="Endereço")
        self.tree.pack(pady=10, fill="x")

        self.tree.bind("<Double-1>", self.on_tree_select)

        self.atualizar_tabela_fornecedores()

    def atualizar_tabela_fornecedores(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for fornecedor in self.db.buscar_fornecedores():
            self.tree.insert("", "end", values=(
                fornecedor["RazaoSocial"], fornecedor["CNPJ"], fornecedor["Email"], fornecedor["Telefone"], fornecedor["Endereco"]
            ))

    def on_tree_select(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, "values")
        self.entry_nome.delete(0, ctk.END)
        self.entry_nome.insert(0, valores[0])
        self.entry_cnpj.delete(0, ctk.END)
        self.entry_cnpj.insert(0, valores[1])
        self.entry_email.delete(0, ctk.END)
        self.entry_email.insert(0, valores[2])
        self.entry_telefone.delete(0, ctk.END)
        self.entry_telefone.insert(0, valores[3])
        self.entry_endereco.delete(0, ctk.END)
        self.entry_endereco.insert(0, valores[4])
    
        self.btn_salvar.grid_remove()

    def salvar(self):
        razao_social = self.entry_nome.get().strip()
        cnpj = self.entry_cnpj.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not razao_social or not cnpj:
            messagebox.showwarning("Atenção", "Razão Social e CNPJ são obrigatórios!")
            return

        # Verifica se já existe fornecedor com esse CNPJ
        fornecedores = self.db.buscar_fornecedores()
        fornecedor = next((f for f in fornecedores if f["CNPJ"] == cnpj), None)

        if fornecedor is None:
            sucesso = self.db.inserir_fornecedor(razao_social, cnpj, email, telefone, endereco)
            if sucesso:
                messagebox.showinfo("Sucesso", "Fornecedor inserido com sucesso!")
                self.limpar()
            else:
                messagebox.showerror("Erro", "Erro ao inserir fornecedor.")
        else:
            # Atualizar fornecedor existente
            try:
                sucesso = self.db.atualizar_fornecedor(
                    fornecedor["Id"], razao_social, cnpj, email, telefone, endereco
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
                    self.limpar()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar fornecedor.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar fornecedor: {e}")

    def buscar(self):
        cnpj = self.entry_cnpj.get().strip()
        if cnpj == "":
            messagebox.showwarning("Atenção", "Informe o CNPJ para buscar!")
            return

        fornecedores = self.db.buscar_fornecedores()
        fornecedor = next((f for f in fornecedores if f["CNPJ"] == cnpj), None)
        if fornecedor:
            self.entry_nome.delete(0, ctk.END)
            self.entry_nome.insert(0, fornecedor["RazaoSocial"])
            self.entry_cnpj.delete(0, ctk.END)
            self.entry_cnpj.insert(0, fornecedor["CNPJ"])
            self.entry_email.delete(0, ctk.END)
            self.entry_email.insert(0, fornecedor["Email"])
            self.entry_telefone.delete(0, ctk.END)
            self.entry_telefone.insert(0, fornecedor["Telefone"])
            self.entry_endereco.delete(0, ctk.END)
            self.entry_endereco.insert(0, fornecedor["Endereco"])
        else:
            messagebox.showinfo("Buscar", "Fornecedor não encontrado!")

    def deletar(self):
        cnpj = self.entry_cnpj.get().strip()
        if cnpj == "":
            messagebox.showwarning("Atenção", "Informe o CNPJ para deletar!")
            return

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que quer deletar este fornecedor?")
        if not confirm:
            return

        fornecedores = self.db.buscar_fornecedores()
        fornecedor = next((f for f in fornecedores if f["CNPJ"] == cnpj), None)
        if fornecedor:
            sucesso = self.db.deletar_fornecedor(fornecedor["Id"])
            if sucesso:
                messagebox.showinfo("Sucesso", "Fornecedor deletado com sucesso!")
                self.limpar()
            else:
                messagebox.showerror("Erro", "Erro ao deletar fornecedor.")
        else:
            messagebox.showinfo("Buscar", "Fornecedor não encontrado!")

    def limpar(self):
        self.btn_salvar.grid()  # Mostra novamente o botão Salvar
        self.entry_nome.delete(0, ctk.END)
        self.entry_cnpj.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)
        self.atualizar_tabela_fornecedores()

    def atualizar(self):
        razao_social = self.entry_nome.get().strip()
        cnpj = self.entry_cnpj.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not razao_social or not cnpj:
            messagebox.showwarning("Atenção", "Razão Social e CNPJ são obrigatórios!")
            return

        fornecedores = self.db.buscar_fornecedores()
        fornecedor = next((f for f in fornecedores if f["CNPJ"] == cnpj), None)

        if fornecedor:
            sucesso = self.db.atualizar_fornecedor(
                fornecedor["Id"], razao_social, cnpj, email, telefone, endereco
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
                self.limpar()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar fornecedor.")
        else:
            messagebox.showinfo("Atualizar", "Fornecedor não encontrado para atualizar.")

        self.atualizar_tabela_fornecedores()
