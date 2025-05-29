class Produto:
    # Construtor vazio
    def __init__(self, id=None, nome="", codigo_barras="", preco=0.0, quantidade_estoque=0, descricao="", fornecedor_padrao_id=None):
        self.id = id
        self.nome = nome
        self.codigo_barras = codigo_barras
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.descricao = descricao
        self.fornecedor_padrao_id = fornecedor_padrao_id

    def __str__(self):
        return (f"Produto({self.id}, {self.nome}, {self.codigo_barras}, {self.preco}, "
                f"{self.quantidade_estoque}, {self.descricao}, {self.fornecedor_padrao_id})")

    def exibir(self):
        print(f"ID: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Código de Barras: {self.codigo_barras}")
        print(f"Preço: {self.preco}")
        print(f"Quantidade em Estoque: {self.quantidade_estoque}")
        print(f"Descrição: {self.descricao}")
        print(f"Fornecedor Padrão ID: {self.fornecedor_padrao_id}")