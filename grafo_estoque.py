import customtkinter as ctk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector

class GrafoEstoque(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Grafo de Produtos e Fornecedores")
        self.geometry("700x500")
        self.grab_set()

        self.fig, self.ax = plt.subplots(figsize=(7,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.montar_grafo()

    def conectar_bd(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="controleestoque"
        )

    def montar_grafo(self):
        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()

            # Consulta produtos e seus fornecedores
            cursor.execute("SELECT Nome, FornecedorPadraoId FROM produto")
            dados = cursor.fetchall()

            # Consulta nomes dos fornecedores (usar RazaoSocial no lugar de Nome)
            cursor.execute("SELECT Id, RazaoSocial FROM fornecedor")
            fornecedores = {f[0]: f[1] for f in cursor.fetchall()}

            cursor.close()
            conexao.close()

            if not dados:
                messagebox.showinfo("Info", "Nenhum dado para exibir no grafo.")
                return

            G = nx.Graph()

            # Adiciona nós e arestas
            for produto, fornecedor_id in dados:
                fornecedor_nome = fornecedores.get(fornecedor_id, f"Fornecedor {fornecedor_id}")
                G.add_node(produto, type='produto')
                G.add_node(fornecedor_nome, type='fornecedor')
                G.add_edge(produto, fornecedor_nome)

            self.ax.clear()

            # Layout do grafo
            pos = nx.spring_layout(G)

            # Nós do tipo produto
            produtos = [n for n, attr in G.nodes(data=True) if attr['type']=='produto']
            # Nós do tipo fornecedor
            fornecedores_nos = [n for n, attr in G.nodes(data=True) if attr['type']=='fornecedor']

            nx.draw_networkx_nodes(G, pos, nodelist=produtos, node_color='skyblue', label='Produtos', node_size=700)
            nx.draw_networkx_nodes(G, pos, nodelist=fornecedores_nos, node_color='lightgreen', label='Fornecedores', node_size=700)
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, pos, font_size=8)

            self.ax.legend()
            self.ax.set_axis_off()

            self.canvas.draw()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao carregar dados do grafo: {err}")
