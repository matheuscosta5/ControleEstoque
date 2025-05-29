import mysql.connector

class Conexao:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'ControleEstoque'
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conexao
        except mysql.connector.Error as e:
            print(f"Erro ao conectar: {e}")
            return None

    def desconectar(self):
        if self.conexao:
            self.conexao.close()

    # CRUD - Exemplo para tabela Cliente
    def inserir_cliente(self, nome, cpf, email, telefone, endereco):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "INSERT INTO Cliente (Nome, CPF, Email, Telefone, Endereco) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome, cpf, email, telefone, endereco))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao inserir cliente: {e}")
            return False

    def buscar_clientes(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Cliente")
            resultados = cursor.fetchall()
            cursor.close()
            self.desconectar()
            return resultados
        except mysql.connector.Error as e:
            print(f"Erro ao buscar clientes: {e}")
            return []

    def atualizar_cliente(self, id, nome, cpf, email, telefone, endereco):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "UPDATE Cliente SET Nome=%s, CPF=%s, Email=%s, Telefone=%s, Endereco=%s WHERE Id=%s"
            cursor.execute(sql, (nome, cpf, email, telefone, endereco, id))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar cliente: {e}")
            return False

    def deletar_cliente(self, id):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "DELETE FROM Cliente WHERE Id=%s"
            cursor.execute(sql, (id,))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao deletar cliente: {e}")
            return False

    # CRUD - Fornecedor
    def inserir_fornecedor(self, razao_social, cnpj, email, telefone, endereco):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "INSERT INTO Fornecedor (RazaoSocial, CNPJ, Email, Telefone, Endereco) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (razao_social, cnpj, email, telefone, endereco))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao inserir fornecedor: {e}")
            return False

    def buscar_fornecedores(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Fornecedor")
            resultados = cursor.fetchall()
            cursor.close()
            self.desconectar()
            return resultados
        except mysql.connector.Error as e:
            print(f"Erro ao buscar fornecedores: {e}")
            return []

    def atualizar_fornecedor(self, id, razao_social, cnpj, email, telefone, endereco):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "UPDATE Fornecedor SET RazaoSocial=%s, CNPJ=%s, Email=%s, Telefone=%s, Endereco=%s WHERE Id=%s"
            cursor.execute(sql, (razao_social, cnpj, email, telefone, endereco, id))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar fornecedor: {e}")
            return False

    def deletar_fornecedor(self, id):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "DELETE FROM Fornecedor WHERE Id=%s"
            cursor.execute(sql, (id,))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao deletar fornecedor: {e}")
            return False

    # CRUD - Produto
    def inserir_produto(self, nome, codigo_barras, preco, quantidade_estoque, descricao, fornecedor_padrao_id):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = """INSERT INTO Produto (Nome, CodigoBarras, Preco, QuantidadeEstoque, Descricao, FornecedorPadraoId)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (nome, codigo_barras, preco, quantidade_estoque, descricao, fornecedor_padrao_id))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao inserir produto: {e}")
            return False

    def buscar_produtos(self):
        try:
            conn = self.conectar()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Produto")
            resultados = cursor.fetchall()
            cursor.close()
            self.desconectar()
            return resultados
        except mysql.connector.Error as e:
            print(f"Erro ao buscar produtos: {e}")
            return []

    def atualizar_produto(self, id, nome, codigo_barras, preco, quantidade_estoque, descricao, fornecedor_padrao_id):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = """UPDATE Produto SET Nome=%s, CodigoBarras=%s, Preco=%s, QuantidadeEstoque=%s, 
                     Descricao=%s, FornecedorPadraoId=%s WHERE Id=%s"""
            cursor.execute(sql, (nome, codigo_barras, preco, quantidade_estoque, descricao, fornecedor_padrao_id, id))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar produto: {e}")
            return False

    def deletar_produto(self, id):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "DELETE FROM Produto WHERE Id=%s"
            cursor.execute(sql, (id,))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao deletar produto: {e}")
            return False

    # CRUD - Estoque (sem exclusão física, apenas flag Ativo)
    def inserir_estoque(self, tipo_movimentacao, quantidade, produto_id, fornecedor_id, cliente_id, observacao):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = """INSERT INTO Estoque (TipoMovimentacao, Quantidade, ProdutoId, FornecedorId, ClienteId, Observacao)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (tipo_movimentacao, quantidade, produto_id, fornecedor_id, cliente_id, observacao))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao inserir movimentação de estoque: {e}")
            return False

    def buscar_estoque(self, apenas_ativos=True):
        try:
            conn = self.conectar()
            cursor = conn.cursor(dictionary=True)
            if apenas_ativos:
                cursor.execute("SELECT * FROM Estoque WHERE Ativo = TRUE")
            else:
                cursor.execute("SELECT * FROM Estoque")
            resultados = cursor.fetchall()
            cursor.close()
            self.desconectar()
            return resultados
        except mysql.connector.Error as e:
            print(f"Erro ao buscar estoque: {e}")
            return []

    def atualizar_estoque(self, id, tipo_movimentacao, quantidade, produto_id, fornecedor_id, cliente_id, observacao):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = """UPDATE Estoque SET TipoMovimentacao=%s, Quantidade=%s, ProdutoId=%s, 
                     FornecedorId=%s, ClienteId=%s, Observacao=%s WHERE Id=%s"""
            cursor.execute(sql, (tipo_movimentacao, quantidade, produto_id, fornecedor_id, cliente_id, observacao, id))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao atualizar movimentação de estoque: {e}")
            return False

    def inativar_estoque(self, id):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = "UPDATE Estoque SET Ativo = FALSE WHERE Id=%s"
            cursor.execute(sql, (id,))
            conn.commit()
            cursor.close()
            self.desconectar()
            return True
        except mysql.connector.Error as e:
            print(f"Erro ao inativar movimentação de estoque: {e}")
            return False
