-- Script de criação do banco de dados

CREATE TABLE IF NOT EXISTS usuarios (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Usuario TEXT UNIQUE NOT NULL,
    Senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quadros (
    IdQuadro INTEGER PRIMARY KEY AUTOINCREMENT,
    IdUsuarioDono INT, 
    IdQuadroSala VARCHAR(50) UNIQUE,
    FOREIGN KEY (IdUsuarioDono) REFERENCES usuarios(id) 
);

CREATE TABLE IF NOT EXISTS elementos (
    IdElemento INTEGER PRIMARY KEY AUTOINCREMENT,
    IdQuadro INT, 
    Tipo TEXT CHECK(Tipo IN ('Retangulo', 'Quadrado', 'Circulo', 'Triangulo', 'Linha', 'Seta', 'Texto')), 
    PosX INT,
    PosY INT,
    Largura INT,
    Altura INT, 
    Cor INT,
    Texto VARCHAR(50),
    Versao INT,
    FOREIGN KEY (IdQuadro) REFERENCES quadros(IdQuadro) 
);

CREATE TABLE IF NOT EXISTS usuarioQuadro (
    IdUsuario INT,
    IdQuadro INT, 
	FOREIGN KEY (IdUsuario) REFERENCES usuarios(id),
    FOREIGN KEY (IdQuadro) REFERENCES quadros(IdQuadro) 
);
