import customtkinter as ctk
from datetime import datetime
from Conexao import Conexao

class ChatbotIAJanela(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Chatbot IA - Controle de Estoque")
        self.geometry("600x500")

        # Conexão com o banco de dados SQLite
        self.db = Conexao()  # Instancia a conexão

        # Exemplo de dados de estoque
        self.produtos = [
            {"nome": "Mouse Gamer", "quantidade": 50, "fornecedor": "TechDistrib", "ultima_entrada": "27/05/2025 15:47"},
            {"nome": "Teclado Mecânico RGB", "quantidade": 30, "fornecedor": "InfoParts", "ultima_entrada": "25/05/2025 10:20"},
            {"nome": "Monitor 24\"", "quantidade": 20, "fornecedor": "FastEletrônicos", "ultima_entrada": "20/05/2025 09:00"},
        ]
        self.fornecedores = ["TechDistrib", "InfoParts", "FastEletrônicos"]

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
            produtos = self.db.buscar_produtos()
            total = sum(prod["QuantidadeEstoque"] for prod in produtos)
            return f"Temos atualmente {total} produtos em estoque."
        elif "última entrada" in pergunta:
            estoque = self.db.buscar_estoque()
            entradas = [e for e in estoque if e["TipoMovimentacao"] == "ENTRADA"]
            if entradas:
                ultima = max(entradas, key=lambda x: x["DataMovimentacao"])
                # Buscar nome do produto
                produtos = self.db.buscar_produtos()
                prod_nome = next((p["Nome"] for p in produtos if p["Id"] == ultima["ProdutoId"]), "Desconhecido")
                return f"A última entrada foi em {ultima['DataMovimentacao']} para o produto '{prod_nome}'."
            else:
                return "Nenhuma entrada encontrada."
        elif "fornecedores" in pergunta:
            fornecedores = self.db.buscar_fornecedores()
            nomes = [f["RazaoSocial"] for f in fornecedores]
            return f"Temos {len(nomes)} fornecedores cadastrados: {', '.join(nomes)}."
        elif "mais saídas" in pergunta:
            estoque = self.db.buscar_estoque()
            saidas = [e for e in estoque if e["TipoMovimentacao"] == "SAIDA"]
            if saidas:
                # Conta saídas por produto
                from collections import Counter
                contagem = Counter(e["ProdutoId"] for e in saidas)
                mais_vendido_id = contagem.most_common(1)[0][0]
                produtos = self.db.buscar_produtos()
                prod_nome = next((p["Nome"] for p in produtos if p["Id"] == mais_vendido_id), "Desconhecido")
                return f"O produto com mais saídas este mês foi o '{prod_nome}'."
            else:
                return "Nenhuma saída registrada."
        elif "hora" in pergunta:
            return f"Agora são {datetime.now().strftime('%H:%M:%S')}."
        elif "quantidade do produto" in pergunta:
            produtos = self.db.buscar_produtos()
            for prod in produtos:
                if prod["Nome"].lower() in pergunta:
                    return f"O produto '{prod['Nome']}' tem {prod['QuantidadeEstoque']} unidades em estoque."
            return "Não encontrei esse produto no estoque."
        else:
            return "Desculpe, ainda estou aprendendo. Tente perguntar algo sobre estoque, entradas ou saídas."
