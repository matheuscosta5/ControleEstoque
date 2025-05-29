class Fornecedor:
    def __init__(self, id=None, razao_social="", cnpj="", email="", telefone="", endereco=""):
        self.id = id
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def __str__(self):
        return f"Fornecedor({self.id}, {self.razao_social}, {self.cnpj}, {self.email}, {self.telefone}, {self.endereco})"

    # Exemplo de método para exibir os dados
    def exibir(self):
        print(f"ID: {self.id}")
        print(f"Razão Social: {self.razao_social}")
        print(f"CNPJ: {self.cnpj}")
        print(f"Email: {self.email}")
        print(f"Telefone: {self.telefone}")
        print(f"Endereço: {self.endereco}")