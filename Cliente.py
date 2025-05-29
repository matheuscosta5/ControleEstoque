class Cliente:
    # Construtor vazio
    def __init__(self, id=None, nome="", cpf="", email="", telefone="", endereco=""):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def __str__(self):
        return f"Cliente({self.id}, {self.nome}, {self.cpf}, {self.email}, {self.telefone}, {self.endereco})"

    def exibir(self):
        print(f"ID: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Email: {self.email}")
        print(f"Telefone: {self.telefone}")
        print(f"Endereço: {self.endereco}")