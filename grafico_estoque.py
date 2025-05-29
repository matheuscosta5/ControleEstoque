import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector

class GraficoEstoque(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gráfico de Estoque")
        self.geometry("600x800")
        self.grab_set()

        self.fig, self.ax = plt.subplots(figsize=(6,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.plotar_grafico()

    def conectar_bd(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ControleEstoque"
        )

    def plotar_grafico(self):
        try:
            conexao = self.conectar_bd()
            cursor = conexao.cursor()
            cursor.execute("SELECT Nome, QuantidadeEstoque FROM Produto")
            dados = cursor.fetchall()
            cursor.close()
            conexao.close()

            if not dados:
                messagebox.showinfo("Info", "Nenhum dado para exibir no gráfico.")
                return

            nomes = [item[0] for item in dados]
            quantidades = [item[1] for item in dados]

            self.ax.clear()
            self.ax.bar(nomes, quantidades)
            self.ax.set_title("Quantidade em Estoque por Produto")
            self.ax.set_ylabel("Quantidade")
            self.ax.set_xlabel("Produto")
            self.ax.tick_params(axis='x', rotation=45)

            self.canvas.draw()

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao carregar dados do gráfico: {err}")