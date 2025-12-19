USE SalonDB
GO

-- Modulo CITAS

-- 14. Estado_Cita
CREATE TABLE Estado_Cita (
    estado_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_estado VARCHAR(50) UNIQUE NOT NULL 
);

INSERT INTO Estado_Cita (nombre_estado) VALUES
('Pendiente'),
('Confirmada'),
('En Proceso'),
('Completada'),
('Cancelada'),
('No Asistió'),
('Reprogramada');

-- 15. Citas
CREATE TABLE Citas (
    cita_id INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id INT NOT NULL,
    empleado_id INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL,
    estado_id INT NOT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id),
    FOREIGN KEY (estado_id) REFERENCES Estado_Cita(estado_id),
    CHECK (fecha_hora_fin > fecha_hora_inicio)
);

-- 16. Detalle_Cita (Para citas con múltiples servicios)
CREATE TABLE Detalle_Cita (
    detalle_cita_id INT IDENTITY(1,1) PRIMARY KEY,
    cita_id INT NOT NULL,
    servicio_id INT NOT NULL,
    precio_cobrado DECIMAL(10, 2) NOT NULL, -- Precio al momento de la cita
    duracion_real_minutos INT,
    FOREIGN KEY (cita_id) REFERENCES Citas(cita_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id)
        ON UPDATE CASCADE
);

-- 17. Cancelaciones
CREATE TABLE Cancelaciones (
    cancelacion_id INT IDENTITY(1,1) PRIMARY KEY,
    cita_id INT UNIQUE NOT NULL,
    fecha_cancelacion DATETIME DEFAULT GETDATE(),
    motivo VARCHAR(255) NOT NULL,
    cancelado_por VARCHAR(50) NOT NULL, -- Ej. 'Cliente', 'Salón', 'Sistema'
    FOREIGN KEY (cita_id) REFERENCES Citas(cita_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);