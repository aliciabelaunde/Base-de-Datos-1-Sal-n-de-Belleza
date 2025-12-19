USE SalonDB
GO

-- Modulo EMPLEADOS

-- 3. Roles_Empleado
CREATE TABLE Roles_Empleado (
    rol_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO Roles_Empleado (nombre_rol) VALUES
('Administrador'),
('Gerente'),
('Recepcionista'),
('Estilista'),
('Colorista'),
('Barbero'),
('Pedicurista'),
('Cosmetóloga'),
('Maquillista'),
('Masajista'),
('Especialista en Cejas y Pestañas'),
('Auxiliar de Estética'),
('Encargado de Caja'),
('Limpieza');

-- 4. Empleados
CREATE TABLE Empleados (
    empleado_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    rol_id INT NOT NULL,
    fecha_contratacion DATE DEFAULT GETDATE(),
    activo BIT DEFAULT 1, -- 1 = TRUE, 0 = FALSE
    FOREIGN KEY (rol_id) REFERENCES Roles_Empleado(rol_id)
        ON UPDATE CASCADE
);


INSERT INTO Empleados (nombre, apellido, telefono, email, rol_id) VALUES
('Laura', 'Gómez', '5551000001', 'laura.gomez@salon.com', 10), 
('Marcos', 'Pineda', '5551000002', 'marcos.pineda@salon.com', 21),
('Daniela', 'Rojas', '5551000003', 'daniela.rojas@salon.com', 15), 
('Andrea', 'Morales', '5551000004', 'andrea.morales@salon.com', 20),
('Sofía', 'Luna', '5551000005', 'sofia.luna@salon.com', 1),
('Paola', 'Vega', '5551000006', 'paola.vega@salon.com', 18),
('Ricardo', 'Salinas', '5551000007', 'ricardo.salinas@salon.com', 12),
('Ana', 'Herrera', '5551000008', 'ana.herrera@salon.com', 16),
('Carlos', 'Medina', '5551000009', 'carlos.medina@salon.com', 19),
('Marta', 'Silva', '5551000010', 'marta.silva@salon.com', 17);


-- 5. Especialidades
CREATE TABLE Especialidades (
    especialidad_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_especialidad VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO Especialidades (nombre_especialidad) VALUES
('Corte de Cabello'),
('Corte Femenino'),
('Corte Masculino'),
('Coloración'),
('Balayage'),
('Mechas'),
('Alisado'),
('Keratina'),
('Peinados'),
('Peinados para Eventos'),
('Maquillaje'),
('Maquillaje Profesional'),
('Maquillaje Social'),
('Manicure'),
('Pedicure'),
('Uñas Acrílicas'),
('Uñas Gel'),
('Nail Art'),
('Diseño de Cejas'),
('Lifting de Pestañas'),
('Extensión de Pestañas'),
('Depilación Facial'),
('Depilación Corporal'),
('Tratamientos Faciales'),
('Tratamientos Corporales'),
('Masajes Relajantes'),
('Masajes Reductivos'),
('Limpieza Facial'),
('Tratamientos Capilares'),
('Asesoría de Imagen');

-- 6. Empleado_Especialidad (Tabla de relación M:M)
CREATE TABLE Empleado_Especialidad (
    empleado_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    PRIMARY KEY (empleado_id, especialidad_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (especialidad_id) REFERENCES Especialidades(especialidad_id)
        ON UPDATE CASCADE
);

-- 7. Horarios_Empleado
CREATE TABLE Horarios_Empleado (
    horario_id INT IDENTITY(1,1) PRIMARY KEY,
    empleado_id INT NOT NULL,
    dia_semana INT NOT NULL CHECK (dia_semana BETWEEN 1 AND 7), -- Lunes=1 a Domingo=7 
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    UNIQUE (empleado_id, dia_semana),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
