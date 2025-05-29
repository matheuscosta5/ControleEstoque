import google.generativeai as genai

# Configura a API da Google (Gemini)
genai.configure(api_key="...")

# Cria uma instância persistente de chat
model = genai.GenerativeModel("gemini-1.5-flash")  # ou "gemini-pro"
chat = model.start_chat()

def enviar_mensagem(pergunta):
    try:
        resposta = chat.send_message(pergunta)
        return resposta.text
    except Exception as e:
        return f"Erro ao consultar a IA:\n{e}"
