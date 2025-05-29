-- Criação do banco de dados
CREATE DATABASE ControleEstoque;
USE ControleEstoque;

-- Tabela Cliente
CREATE TABLE Cliente (
    Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CPF VARCHAR(14) UNIQUE NOT NULL,
    Email VARCHAR(100),
    Telefone VARCHAR(15) NOT NULL,
    Endereco VARCHAR(200)
);

-- Tabela Fornecedor
CREATE TABLE Fornecedor (
    Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    RazaoSocial VARCHAR(100) NOT NULL,
    CNPJ VARCHAR(18) UNIQUE NOT NULL,
    Email VARCHAR(100),
    Telefone VARCHAR(15) NOT NULL,
    Endereco VARCHAR(200)
);

-- Tabela Produto
CREATE TABLE Produto (
    Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CodigoBarras VARCHAR(50) UNIQUE,
    Preco DECIMAL(10,2) NOT NULL,
    QuantidadeEstoque INT NOT NULL DEFAULT 0,
    Descricao TEXT,
    FornecedorPadraoId INT NULL,
    FOREIGN KEY (FornecedorPadraoId) REFERENCES Fornecedor(Id)
);

-- Tabela Estoque (com flag de registro ativo)
CREATE TABLE Estoque (
    Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    TipoMovimentacao ENUM('ENTRADA', 'SAIDA') NOT NULL,
    Quantidade INT NOT NULL,
    DataMovimentacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Ativo BOOLEAN NOT NULL DEFAULT TRUE,
    Observacao TEXT,
    
    -- Chaves estrangeiras
    ClienteId INT NULL,
    FornecedorId INT NULL,
    ProdutoId INT NOT NULL,
    
    FOREIGN KEY (ClienteId) REFERENCES Cliente(Id),
    FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id),
    FOREIGN KEY (ProdutoId) REFERENCES Produto(Id)
);

-- Índices para melhorar performance
CREATE INDEX idx_estoque_produto ON Estoque(ProdutoId);
CREATE INDEX idx_estoque_data ON Estoque(DataMovimentacao);

-- Inserindo clientes
INSERT INTO Cliente (Nome, CPF, Email, Telefone, Endereco) VALUES
('João Silva', '123.456.789-00', 'joao@email.com', '(11) 9999-8888', 'Rua A, 123 - São Paulo'),
('Maria Santos', '987.654.321-00', 'maria@email.com', '(11) 7777-6666', 'Av. B, 456 - São Paulo');

-- Inserindo fornecedores
INSERT INTO Fornecedor (RazaoSocial, CNPJ, Email, Telefone, Endereco) VALUES
('Fornecedor ABC LTDA', '12.345.678/0001-00', 'abc@fornecedor.com', '(11) 3333-2222', 'Rua Industrial, 100'),
('Distribuidora XYZ S/A', '98.765.432/0001-00', 'xyz@distribuidora.com', '(11) 4444-5555', 'Av. Comercial, 200');

-- Inserindo produtos
INSERT INTO Produto (Nome, CodigoBarras, Preco, QuantidadeEstoque, Descricao, FornecedorPadraoId) VALUES
('Notebook Dell', '7891234567890', 3500.00, 10, 'Notebook Dell i5 8GB RAM', 1),
('Mouse Sem Fio', '7899876543210', 120.50, 50, 'Mouse óptico sem fio', 2),
('Teclado Mecânico', '7894561237890', 250.00, 30, 'Teclado mecânico RGB', 1);

-- Registrando movimentações no estoque
INSERT INTO Estoque (TipoMovimentacao, Quantidade, ProdutoId, FornecedorId, Observacao) VALUES
('ENTRADA', 10, 1, 1, 'Compra inicial de estoque'),
('ENTRADA', 50, 2, 2, 'Compra inicial de estoque'),
('ENTRADA', 30, 3, 1, 'Compra inicial de estoque'),
('SAIDA', 1, 1, 1, 'Venda para cliente João Silva'),
('SAIDA', 2, 3, 1, 'Venda para cliente João Silva'),
('SAIDA', 3, 2, 2, 'Venda para cliente Maria Santos');

-- Consultando todos os clientes
SELECT * FROM Cliente;

-- Consultando todos os fornecedores
SELECT * FROM Fornecedor;

-- Consultando todos os produtos
SELECT * FROM Produto;


-- Consultando movimentações de estoque
SELECT * FROM Estoque;

-- Produtos e seus fornecedores padrão
SELECT p.Nome AS Produto, f.RazaoSocial AS FornecedorPadrao
FROM Produto p
LEFT JOIN Fornecedor f ON p.FornecedorPadraoId = f.Id;

-- Movimentações de estoque com detalhes completos
SELECT 
    e.DataMovimentacao,
    CASE e.TipoMovimentacao 
        WHEN 'ENTRADA' THEN 'Entrada' 
        WHEN 'SAIDA' THEN 'Saída' 
    END AS Tipo,
    p.Nome AS Produto,
    e.Quantidade,
    f.RazaoSocial AS Fornecedor,
    c.Nome AS Cliente,
    e.Observacao
FROM Estoque e
JOIN Produto p ON e.ProdutoId = p.Id
LEFT JOIN Fornecedor f ON e.FornecedorId = f.Id
LEFT JOIN Cliente c ON e.ClienteId = c.Id
ORDER BY e.DataMovimentacao DESC;

-- Marcando uma movimentação de estoque como inativa (exclusão lógica)
UPDATE Estoque SET Ativo = FALSE WHERE Id = 4;

-- Consultando para verificar a exclusão (mostra apenas registros ativos)
SELECT * FROM Estoque WHERE Ativo = TRUE;

-- Consultando todos os registros, incluindo os inativos
SELECT * FROM Estoque;

-- Relatório de produtos mais vendidos
SELECT 
    p.Nome AS Produto,
    SUM(CASE WHEN e.TipoMovimentacao = 'SAIDA' THEN e.Quantidade ELSE 0 END) AS TotalVendido,
    SUM(CASE WHEN e.TipoMovimentacao = 'ENTRADA' THEN e.Quantidade ELSE 0 END) AS TotalEstocado,
    p.QuantidadeEstoque AS EstoqueAtual
FROM Produto p
LEFT JOIN Estoque e ON p.Id = e.ProdutoId AND e.Ativo = TRUE
GROUP BY p.Id
ORDER BY TotalVendido DESC;

-- Relatório de fornecedores e seus produtos
SELECT 
    f.RazaoSocial AS Fornecedor,
    COUNT(DISTINCT p.Id) AS 'Qtd Produtos Fornecidos',
    SUM(p.QuantidadeEstoque) AS 'Total em Estoque'
FROM Fornecedor f
LEFT JOIN Produto p ON f.Id = p.FornecedorPadraoId
GROUP BY f.Id;

-- Histórico completo de um produto específico
SELECT 
    e.DataMovimentacao,
    CASE e.TipoMovimentacao 
        WHEN 'ENTRADA' THEN CONCAT('Entrada (', f.RazaoSocial, ')') 
        WHEN 'SAIDA' THEN CONCAT('Saída (', c.Nome, ')') 
    END AS Movimentacao,
    e.Quantidade,
    e.Observacao
FROM Estoque e
LEFT JOIN Fornecedor f ON e.FornecedorId = f.Id
LEFT JOIN Cliente c ON e.ClienteId = c.Id
WHERE e.ProdutoId = 1 AND e.Ativo = TRUE
ORDER BY e.DataMovimentacao;

-- Verificar que todos estão inativos
SELECT COUNT(*) AS 'Registros Ativos' FROM Estoque WHERE Ativo = TRUE;