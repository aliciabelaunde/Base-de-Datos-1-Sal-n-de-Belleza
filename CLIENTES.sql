USE SalonDB
GO

-- Modulo CLIENTES

-- 1. Clientes
CREATE TABLE Clientes (
    cliente_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    fecha_registro DATE DEFAULT GETDATE()
);

INSERT INTO Clientes (nombre, apellido, telefono, email) VALUES 
('Ana', 'García', '5551234567', 'ana.garcia@email.com'),
('Carlos', 'Pérez', '5559876543', 'carlos.perez@email.com'),
('María', 'López', '5554567890', 'maria.lopez@email.com'),
('Juan', 'Martínez', '5553219876', 'juan.martinez@email.com');

INSERT INTO Clientes (nombre, apellido, telefono, email) VALUES
('Lucía', 'Fernández', '5550000015', 'lucia.fernandez@email.com'),
('Miguel', 'Torres', '5550000016', 'miguel.torres@email.com'),
('Sofía', 'Hernández', '5550000017', 'sofia.hernandez@email.com'),
('Diego', 'Ruiz', '5550000018', 'diego.ruiz@email.com'),
('Valentina', 'Castro', '5550000019', 'valentina.castro@email.com'),
('Andrés', 'Morales', '5550000020', 'andres.morales@email.com'),
('Camila', 'Ortega', '5550000021', 'camila.ortega@email.com'),
('Fernando', 'Navarro', '5550000022', 'fernando.navarro@email.com'),
('Paula', 'Ríos', '5550000023', 'paula.rios@email.com'),
('Javier', 'Mendoza', '5550000024', 'javier.mendoza@email.com');

-- 2. Detalles_Cliente
CREATE TABLE Detalles_Cliente (
    detalle_cliente_id INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id INT UNIQUE NOT NULL,
    alergias VARCHAR(MAX), 
    contraindicaciones VARCHAR(MAX),
    notas_tecnicas VARCHAR(MAX),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO Detalles_Cliente (cliente_id, alergias, contraindicaciones, notas_tecnicas)
VALUES
(15, 'Fragancias', NULL, 'Piel reactiva'),
(16, NULL, 'Diabetes', 'Evitar sesiones prolongadas'),
(17, 'Látex', 'Embarazo', 'Consulta previa obligatoria'),
(18, NULL, NULL, 'Sin observaciones'),
(30, 'Anestesia', 'Hipotensión', 'Sesión corta'),
(25, 'Polen', NULL, 'Primera visita'),
(21, NULL, 'Asma', 'Ambiente ventilado'),
(22, 'Níquel', NULL, 'Evitar instrumentos metálicos'),
(23, NULL, NULL, 'Cliente frecuente'),
(24, 'Alcohol', 'Piel sensible', 'Usar productos hipoalergénicos');

Select * From Clientes
