USE SalonDB
GO

-- Modulo PROMOCIONES

-- 12. Promociones
CREATE TABLE Promociones (
    promocion_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_promocion VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    porcentaje_descuento DECIMAL(5, 2) NULL CHECK (porcentaje_descuento BETWEEN 0.00 AND 100.00),
    activo BIT DEFAULT 1,
    CHECK (fecha_fin >= fecha_inicio)
);

INSERT INTO Promociones (nombre_promocion, descripcion, fecha_inicio, fecha_fin, porcentaje_descuento, activo) VALUES
('Bienvenido Invierno', 'Descuento general para el inicio de temporada', '2024-06-01', '2024-06-30', 15.00, 1),
('Combo Manicure & Pedicure', 'Ahorra en el cuidado de tus manos y pies', '2024-01-01', '2024-12-31', 20.00, 1),
('Día del Padre', 'Especial para servicios de barbería', '2024-06-15', '2024-06-20', 10.00, 1),
('Black Friday Beauty', 'Gran descuento en servicios seleccionados', '2024-11-20', '2024-11-30', 40.00, 1),
('Aniversario del Salón', 'Descuento en tratamientos capilares', '2024-09-01', '2024-09-15', 25.00, 1);

-- 13. Promocion_Servicio (Relación M:M: qué servicios están incluidos en la promoción)
CREATE TABLE Promocion_Servicio (
    promocion_id INT NOT NULL,
    servicio_id INT NOT NULL,
    PRIMARY KEY (promocion_id, servicio_id),
    FOREIGN KEY (promocion_id) REFERENCES Promociones(promocion_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
