CREATE TABLE tipo(
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(30) NOT NULL
);

CREATE TABLE fecha(
    id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL
);

CREATE TABLE municipio(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE origen(
    id INT PRIMARY KEY AUTO_INCREMENT,
    origen VARCHAR(20) NOT NULL
);

CREATE TABLE colonia(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    id_municipio INT NOT NULL,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id)
);

CREATE TABLE bienraiz(
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL,
    precio VARCHAR(50),
    m2 INT,
    m2_2 INT,
    rooms INT,
    baths INT,
    cars INT,
    descripcion VARCHAR(150),
    id_tipo INT,
    id_origen INT,
    id_colonia INT,
    id_fecha INT,
    FOREIGN KEY (id_tipo) REFERENCES tipo(id),
    FOREIGN KEY (id_origen) REFERENCES origen(id),
    FOREIGN KEY (id_colonia) REFERENCES colonia(id),
    FOREIGN KEY (id_fecha) REFERENCES fecha(id)
);

CREATE TABLE imagen(
    id INT PRIMARY KEY AUTO_INCREMENT,
    ubicacion VARCHAR(100) NOT NULL,
    id_bienraiz INT,
    FOREIGN KEY (id_bienraiz) REFERENCES bienraiz(id)
);