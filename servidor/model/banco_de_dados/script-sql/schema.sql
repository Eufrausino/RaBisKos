-- Script de criação do banco de dados

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

-- Aqui você pode adicionar novas tabelas no futuro
-- CREATE TABLE IF NOT EXISTS mensagens (...);
