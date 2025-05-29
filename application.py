from Conexao import Conexao
from Cliente import Cliente
from Fornecedor import Fornecedor
from Produto import Produto
from Estoque import Estoque

def menu_principal():
    print("\n--- Controle de Estoque ---")
    print("1. Cliente")
    print("2. Fornecedor")
    print("3. Produto")
    print("4. Estoque")
    print("0. Sair")
    return input("Escolha uma opção: ")

def menu_crud(nome):
    print(f"\n--- {nome} ---")
    print("1. Inserir")
    print("2. Listar")
    print("3. Atualizar")
    print("4. Deletar" if nome != "Estoque" else "4. Inativar")
    print("0. Voltar")
    return input("Escolha uma opção: ")

def crud_cliente(conexao):
    while True:
        op = menu_crud("Cliente")
        if op == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            sucesso = conexao.inserir_cliente(nome, cpf, email, telefone, endereco)
            print("Cliente inserido com sucesso!" if sucesso else "Erro ao inserir cliente.")
        elif op == "2":
            clientes = conexao.buscar_clientes()
            for c in clientes:
                print(c)
        elif op == "3":
            id = int(input("ID do cliente a atualizar: "))
            nome = input("Novo Nome: ")
            cpf = input("Novo CPF: ")
            email = input("Novo Email: ")
            telefone = input("Novo Telefone: ")
            endereco = input("Novo Endereço: ")
            sucesso = conexao.atualizar_cliente(id, nome, cpf, email, telefone, endereco)
            print("Cliente atualizado com sucesso!" if sucesso else "Erro ao atualizar cliente.")
        elif op == "4":
            id = int(input("ID do cliente a deletar: "))
            sucesso = conexao.deletar_cliente(id)
            print("Cliente deletado com sucesso!" if sucesso else "Erro ao deletar cliente.")
        elif op == "0":
            break

def crud_fornecedor(conexao):
    while True:
        op = menu_crud("Fornecedor")
        if op == "1":
            razao = input("Razão Social: ")
            cnpj = input("CNPJ: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            sucesso = conexao.inserir_fornecedor(razao, cnpj, email, telefone, endereco)
            print("Fornecedor inserido com sucesso!" if sucesso else "Erro ao inserir fornecedor.")
        elif op == "2":
            fornecedores = conexao.buscar_fornecedores()
            for f in fornecedores:
                print(f)
        elif op == "3":
            id = int(input("ID do fornecedor a atualizar: "))
            razao = input("Nova Razão Social: ")
            cnpj = input("Novo CNPJ: ")
            email = input("Novo Email: ")
            telefone = input("Novo Telefone: ")
            endereco = input("Novo Endereço: ")
            sucesso = conexao.atualizar_fornecedor(id, razao, cnpj, email, telefone, endereco)
            print("Fornecedor atualizado com sucesso!" if sucesso else "Erro ao atualizar fornecedor.")
        elif op == "4":
            id = int(input("ID do fornecedor a deletar: "))
            sucesso = conexao.deletar_fornecedor(id)
            print("Fornecedor deletado com sucesso!" if sucesso else "Erro ao deletar fornecedor.")
        elif op == "0":
            break

def crud_produto(conexao):
    while True:
        op = menu_crud("Produto")
        if op == "1":
            nome = input("Nome: ")
            codigo = input("Código de Barras: ")
            preco = float(input("Preço: "))
            quantidade = int(input("Quantidade em Estoque: "))
            descricao = input("Descrição: ")
            fornecedor_id = input("ID do Fornecedor Padrão (ou deixe vazio): ")
            fornecedor_id = int(fornecedor_id) if fornecedor_id else None
            sucesso = conexao.inserir_produto(nome, codigo, preco, quantidade, descricao, fornecedor_id)
            print("Produto inserido com sucesso!" if sucesso else "Erro ao inserir produto.")
        elif op == "2":
            produtos = conexao.buscar_produtos()
            for p in produtos:
                print(p)
        elif op == "3":
            id = int(input("ID do produto a atualizar: "))
            nome = input("Novo Nome: ")
            codigo = input("Novo Código de Barras: ")
            preco = float(input("Novo Preço: "))
            quantidade = int(input("Nova Quantidade em Estoque: "))
            descricao = input("Nova Descrição: ")
            fornecedor_id = input("Novo ID do Fornecedor Padrão (ou deixe vazio): ")
            fornecedor_id = int(fornecedor_id) if fornecedor_id else None
            sucesso = conexao.atualizar_produto(id, nome, codigo, preco, quantidade, descricao, fornecedor_id)
            print("Produto atualizado com sucesso!" if sucesso else "Erro ao atualizar produto.")
        elif op == "4":
            id = int(input("ID do produto a deletar: "))
            sucesso = conexao.deletar_produto(id)
            print("Produto deletado com sucesso!" if sucesso else "Erro ao deletar produto.")
        elif op == "0":
            break

def crud_estoque(conexao):
    while True:
        op = menu_crud("Estoque")
        if op == "1":
            tipo = input("Tipo Movimentação (ENTRADA/SAIDA): ")
            quantidade = int(input("Quantidade: "))
            produto_id = int(input("ID do Produto: "))
            fornecedor_id = input("ID do Fornecedor (ou deixe vazio): ")
            fornecedor_id = int(fornecedor_id) if fornecedor_id else None
            cliente_id = input("ID do Cliente (ou deixe vazio): ")
            cliente_id = int(cliente_id) if cliente_id else None
            observacao = input("Observação: ")
            sucesso = conexao.inserir_estoque(tipo, quantidade, produto_id, fornecedor_id, cliente_id, observacao)
            print("Movimentação inserida com sucesso!" if sucesso else "Erro ao inserir movimentação.")
        elif op == "2":
            estoque = conexao.buscar_estoque()
            for e in estoque:
                print(e)
        elif op == "3":
            id = int(input("ID da movimentação a atualizar: "))
            tipo = input("Novo Tipo Movimentação (ENTRADA/SAIDA): ")
            quantidade = int(input("Nova Quantidade: "))
            produto_id = int(input("Novo ID do Produto: "))
            fornecedor_id = input("Novo ID do Fornecedor (ou deixe vazio): ")
            fornecedor_id = int(fornecedor_id) if fornecedor_id else None
            cliente_id = input("Novo ID do Cliente (ou deixe vazio): ")
            cliente_id = int(cliente_id) if cliente_id else None
            observacao = input("Nova Observação: ")
            sucesso = conexao.atualizar_estoque(id, tipo, quantidade, produto_id, fornecedor_id, cliente_id, observacao)
            print("Movimentação atualizada com sucesso!" if sucesso else "Erro ao atualizar movimentação.")
        elif op == "4":
            id = int(input("ID da movimentação a inativar: "))
            sucesso = conexao.inativar_estoque(id)
            print("Movimentação inativada com sucesso!" if sucesso else "Erro ao inativar movimentação.")
        elif op == "0":
            break

def main():
    conexao = Conexao()
    while True:
        op = menu_principal()
        if op == "1":
            crud_cliente(conexao)
        elif op == "2":
            crud_fornecedor(conexao)
        elif op == "3":
            crud_produto(conexao)
        elif op == "4":
            crud_estoque(conexao)
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()