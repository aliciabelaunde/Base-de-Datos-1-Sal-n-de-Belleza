USE SalonDB
GO

-- Modulo Productos

-- 18. Proveedores
CREATE TABLE Proveedores (
    proveedor_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_proveedor VARCHAR(100) UNIQUE NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(15)
);

INSERT INTO Proveedores (nombre_proveedor, contacto, telefono) VALUES
('L''Oréal Professionnel', 'Carlos Ruiz', '+54114567890'),
('Schwarzkopf Pro', 'Ana Martínez', '+54119876543'),
('Wella Professionals', 'Elena Gómez', '+54113334445'),
('Sally Beauty Supply', 'Distribuidora Local', '+54112221110'),
('OPI Nails', 'Roberto Sánchez', '+54116667778');

-- 19. Productos
CREATE TABLE Productos (
    producto_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_producto VARCHAR(100) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    proveedor_id INT NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL CHECK (precio_venta > 0),
    stock_actual INT NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    FOREIGN KEY (proveedor_id) REFERENCES Proveedores(proveedor_id)
        ON UPDATE CASCADE
);


INSERT INTO Productos (nombre_producto, descripcion, proveedor_id, precio_venta, stock_actual) VALUES
('Shampoo Keratina 1L', 'Limpieza profunda con aporte de proteína', 5, 35.00, 15),
('Acondicionador Color Vive', 'Protección para cabellos teñidos', 5, 32.00, 10),
('Tinte Igora Royal 7-0', 'Tinte permanente rubio medio', 2, 12.50, 24),
('Laca Extra Fuerte', 'Fijación de larga duración para peinados', 3, 18.00, 8),
('Aceite de Argán 50ml', 'Tratamiento hidratante y brillo', 4, 25.00, 12),
('Esmalte Gel OPI Red', 'Tono clásico de larga duración', 3, 15.00, 20),
('Polvo Decolorante 500g', 'Aclarante de alto rendimiento', 2, 45.00, 5);

-- 20. Movimiento_Inventario
CREATE TABLE Movimiento_Inventario (
    movimiento_id INT IDENTITY(1,1) PRIMARY KEY,
    producto_id INT NOT NULL,
    tipo_movimiento VARCHAR(10) NOT NULL CHECK (tipo_movimiento IN ('ENTRADA', 'SALIDA', 'AJUSTE')),
    cantidad INT NOT NULL CHECK (cantidad != 0),
    fecha_movimiento DATETIME DEFAULT GETDATE(),
    empleado_id INT, -- Quién realizó o registró el movimiento
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
        ON UPDATE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);