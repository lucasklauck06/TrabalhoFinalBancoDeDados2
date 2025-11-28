-- 1. Remoção das tabelas (Ordem Inversa de Criação/Dependência)
-- Removemos primeiro a tabela 'Compras' pois ela possui referências (FK) para Clientes e Produtos
DROP TABLE IF EXISTS Compras;
DROP TABLE IF EXISTS Produtos;
DROP TABLE IF EXISTS Clientes;

-- 2. Criação da tabela Clientes
-- Esquema: Clientes(id, cpf, nome, endereco, cidade, uf, e-mail) [cite: 9]
CREATE TABLE Clientes (
    id SERIAL PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    uf CHAR(2),
    email VARCHAR(150) -- Adaptado de "e-mail" para evitar caracteres especiais
);

-- 3. Criação da tabela Produtos
-- Esquema: Produtos(id, produto, valor, quantidade, tipo) [cite: 11]
CREATE TABLE Produtos (
    id SERIAL PRIMARY KEY,
    produto VARCHAR(150) NOT NULL, -- Nome do produto
    valor NUMERIC(10, 2) NOT NULL, -- Valor monetário
    quantidade INTEGER NOT NULL,
    tipo VARCHAR(50)
);

-- 4. Criação da tabela Compras
-- Esquema: Compras(id, id_produto, data, id_cliente) [cite: 10]
CREATE TABLE Compras (
    id SERIAL PRIMARY KEY,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    
    -- Definindo nomes para as Constraints (Restrições)
    CONSTRAINT fk_compras_cliente 
        FOREIGN KEY (id_cliente) 
        REFERENCES Clientes (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_compras_produto 
        FOREIGN KEY (id_produto) 
        REFERENCES Produtos (id)
        ON DELETE RESTRICT
);