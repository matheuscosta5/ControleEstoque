import customtkinter as ctk
from datetime import datetime

class ChatbotIAJanela(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Chatbot IA - Controle de Estoque")
        self.geometry("600x500")

        self.mensagem_inicial = (
            "Olá! Eu sou o assistente inteligente do sistema de controle de estoque.\n"
            "Você pode me perguntar coisas como:\n"
            "- Quantos produtos temos no estoque?\n"
            "- Qual foi a última entrada de produtos?\n"
            "- Quais fornecedores temos cadastrados?\n"
            "- Qual produto teve mais saídas este mês?\n"
        )

        self.chat_log = ctk.CTkTextbox(self, wrap="word", width=580, height=380)
        self.chat_log.pack(padx=10, pady=10)
        self.chat_log.insert("end", self.mensagem_inicial + "\n\n")
        self.chat_log.configure(state="disabled")

        self.entry_pergunta = ctk.CTkEntry(self, width=460)
        self.entry_pergunta.pack(side="left", padx=(10, 0), pady=(0, 10))

        self.btn_enviar = ctk.CTkButton(self, text="Enviar", command=self.responder_pergunta)
        self.btn_enviar.pack(side="left", padx=10, pady=(0, 10))

    def responder_pergunta(self):
        pergunta = self.entry_pergunta.get()
        if pergunta.strip() == "":
            return

        resposta = self.gerar_resposta(pergunta)

        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", f"Você: {pergunta}\n")
        self.chat_log.insert("end", f"Bot: {resposta}\n\n")
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")

        self.entry_pergunta.delete(0, "end")

    def gerar_resposta(self, pergunta):
        pergunta = pergunta.lower()

        if "quantos produtos" in pergunta or "total de produtos" in pergunta:
            return "Temos atualmente 358 produtos em estoque."
        elif "última entrada" in pergunta:
            return "A última entrada foi em 27/05/2025 às 15:47 para o produto 'Mouse Gamer'."
        elif "fornecedores" in pergunta:
            return "Temos 5 fornecedores cadastrados: TechDistrib, InfoParts, FastEletrônicos, etc."
        elif "mais saídas" in pergunta:
            return "O produto com mais saídas este mês foi o 'Teclado Mecânico RGB'."
        elif "hora" in pergunta:
            return f"Agora são {datetime.now().strftime('%H:%M:%S')}."
        else:
            return "Desculpe, ainda estou aprendendo. Tente perguntar algo sobre estoque, entradas ou saídas."
