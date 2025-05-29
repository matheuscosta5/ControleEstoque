from cliente_gui import ClienteForm
from fornecedor_gui import FornecedorForm
from produto_gui import ProdutoForm
from estoque_gui import EstoqueForm
from grafico_estoque import GraficoEstoque
from grafo_estoque import GrafoEstoque
from gui_chatbot import ChatbotIAJanela  # Importação do Chatbot

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Controle de Estoque")
        self.geometry("600x450")  # Ajuste de altura

        self.frame_main = ctk.CTkFrame(master=self)
        self.frame_main.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(master=self.frame_main, text="Menu Principal", font=("Arial", 24))
        self.label.pack(pady=12)

        self.btn_cliente = ctk.CTkButton(master=self.frame_main, text="Módulo Cliente", command=self.abrir_cliente)
        self.btn_cliente.pack(pady=10)

        self.btn_fornecedor = ctk.CTkButton(master=self.frame_main, text="Módulo Fornecedor", command=self.abrir_fornecedor)
        self.btn_fornecedor.pack(pady=10)

        self.btn_produto = ctk.CTkButton(master=self.frame_main, text="Módulo Produto", command=self.abrir_produto)
        self.btn_produto.pack(pady=10)

        self.btn_estoque = ctk.CTkButton(master=self.frame_main, text="Módulo Estoque", command=self.abrir_estoque)
        self.btn_estoque.pack(pady=10)

        self.btn_grafico_estoque = ctk.CTkButton(master=self.frame_main, text="Gráfico de Estoque", command=self.abrir_grafico_estoque)
        self.btn_grafico_estoque.pack(pady=10)

        self.btn_grafo_estoque = ctk.CTkButton(master=self.frame_main, text="Grafo de Estoque", command=self.abrir_grafo_estoque)
        self.btn_grafo_estoque.pack(pady=10)

        self.btn_chatbot = ctk.CTkButton(master=self.frame_main, text="Chatbot IA", command=self.abrir_chatbot)
        self.btn_chatbot.pack(pady=10)

    def abrir_cliente(self):
        ClienteForm(self)

    def abrir_fornecedor(self):
        FornecedorForm(self)

    def abrir_produto(self):
        ProdutoForm(self)

    def abrir_estoque(self):
        EstoqueForm(self)

    def abrir_grafico_estoque(self):
        GraficoEstoque(self)

    def abrir_grafo_estoque(self):
        GrafoEstoque(self)

    def abrir_chatbot(self):
        ChatbotIAJanela(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
