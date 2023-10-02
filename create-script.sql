CREATE DATABASE uirses;
\c uirses;

CREATE TABLE produtos (
    codigo SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco NUMERIC(10, 2) NOT NULL
);
