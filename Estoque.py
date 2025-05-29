class Estoque:
    # Construtor vazio
    def __init__(
        self,
        id=None,
        tipo_movimentacao="",
        quantidade=0,
        data_movimentacao=None,
        ativo=True,
        observacao="",
        cliente_id=None,
        fornecedor_id=None,
        produto_id=None
    ):
        self.id = id
        self.tipo_movimentacao = tipo_movimentacao  # 'ENTRADA' ou 'SAIDA'
        self.quantidade = quantidade
        self.data_movimentacao = data_movimentacao
        self.ativo = ativo
        self.observacao = observacao
        self.cliente_id = cliente_id
        self.fornecedor_id = fornecedor_id
        self.produto_id = produto_id

    def __str__(self):
        return (f"Estoque({self.id}, {self.tipo_movimentacao}, {self.quantidade}, "
                f"{self.data_movimentacao}, {self.ativo}, {self.observacao}, "
                f"{self.cliente_id}, {self.fornecedor_id}, {self.produto_id})")

    def exibir(self):
        print(f"ID: {self.id}")
        print(f"Tipo Movimentação: {self.tipo_movimentacao}")
        print(f"Quantidade: {self.quantidade}")
        print(f"Data Movimentação: {self.data_movimentacao}")
        print(f"Ativo: {self.ativo}")
        print(f"Observação: {self.observacao}")
        print(f"Cliente ID: {self.cliente_id}")
        print(f"Fornecedor ID: {self.fornecedor_id}")
        print(f"Produto ID: {self.produto_id}")