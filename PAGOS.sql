USE SalonDB;
GO

-- Modulo PAGOS

-- 21. Metodo_Pago
CREATE TABLE Metodo_Pago (
    metodo_pago_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_metodo VARCHAR(100) UNIQUE NOT NULL 
);

INSERT INTO Metodo_Pago (nombre_metodo) VALUES
('Efectivo'),
('Tarjeta de Débito'),
('Tarjeta de Crédito'),
('Transferencia Bancaria'),
('Pago Móvil'),
('Código QR'),
('Vales'),
('Gift Card'),
('Pago Mixto');

-- 22. Ventas
CREATE TABLE Ventas (
    venta_id INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id INT NOT NULL,
    empleado_id INT NOT NULL,
    fecha_venta DATETIME DEFAULT GETDATE(),
    total_bruto DECIMAL(10,2) NOT NULL CHECK (total_bruto >= 0),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);

-- 23. Detalle_Venta
CREATE TABLE Detalle_Venta (
    detalle_venta_id INT IDENTITY(1,1) PRIMARY KEY,
    venta_id INT NOT NULL,
    servicio_id INT NULL,
    producto_id INT NULL,
    promocion_id INT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal_linea DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id)
        ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id),
    FOREIGN KEY (promocion_id) REFERENCES Promociones(promocion_id),
    CHECK (
        (servicio_id IS NOT NULL AND producto_id IS NULL) OR
        (servicio_id IS NULL AND producto_id IS NOT NULL)
    )
);

-- 24. Pagos
CREATE TABLE Pagos (
    pago_id INT IDENTITY(1,1) PRIMARY KEY,
    venta_id INT NOT NULL,
    metodo_pago_id INT NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL CHECK (monto_pagado > 0),
    fecha_pago DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id)
        ON DELETE CASCADE,
    FOREIGN KEY (metodo_pago_id) REFERENCES Metodo_Pago(metodo_pago_id)
);
