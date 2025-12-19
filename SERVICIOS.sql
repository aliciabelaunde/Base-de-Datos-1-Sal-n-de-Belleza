USE SalonDB
GO

-- Modulo SERVICIOS

-- 8. Categorias_Servicio
CREATE TABLE Categorias_Servicio (
    categoria_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_categoria VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO Categorias_Servicio (nombre_categoria) VALUES
('Corte de Cabello'),
('Peinados'),
('Coloración'),
('Tratamientos Capilares'),
('Manicure'),
('Pedicure'),
('Uñas Acrílicas y Gel'),
('Maquillaje'),
('Depilación'),
('Cejas y Pestañas'),
('Barbería'),
('Servicios Especiales');

-- 9. Servicios
CREATE TABLE Servicios (
    servicio_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_servicio VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10, 2) NOT NULL CHECK (precio >= 0.00),
    duracion_minutos INT NOT NULL CHECK (duracion_minutos > 0)
);

INSERT INTO Servicios (nombre_servicio, descripcion, precio, duracion_minutos) VALUES
('Balayage Premium', 'Técnica de aclarado natural con matizante', 85.00, 180),
('Manicure Ruso', 'Limpieza profunda de cutícula y esmaltado permanente', 20.00, 45),
('Pedicure Spa', 'Exfoliación, hidratación y esmaltado', 25.00, 60),
('Uñas Gel X', 'Extensión de uñas con sistema Gel-X', 40.00, 90),
('Maquillaje Social', 'Maquillaje para eventos con pestañas incluidas', 50.00, 60),
('Depilación Cejas', 'Diseño y depilación con cera o hilo', 10.00, 20),
('Lifting de Pestañas', 'Rizado natural de pestañas con keratina', 35.00, 45),
('Barba VIP', 'Ritual de barba con toalla caliente', 12.00, 25),
('Keratina Orgánica', 'Tratamiento alisador sin formol', 100.00, 150);

-- 10. Servicio_Categoria (Relación M:M)
CREATE TABLE Servicio_Categoria (
    servicio_id INT NOT NULL,
    categoria_id INT NOT NULL,
    PRIMARY KEY (servicio_id, categoria_id),
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES Categorias_Servicio(categoria_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 11. Servicio_Especialidad (qué especialidad requiere cada servicio)
CREATE TABLE Servicio_Especialidad (
    servicio_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    PRIMARY KEY (servicio_id, especialidad_id),
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (especialidad_id) REFERENCES Especialidades(especialidad_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

SELECT * FROM Servicios