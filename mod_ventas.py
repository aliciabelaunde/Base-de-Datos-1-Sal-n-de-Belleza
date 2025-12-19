import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import db_conexion 

class VentasFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.carrito = [] 
        self.mapa_clientes = {}
        self.mapa_empleados = {}
        self.mapa_servicios = {}
        self.mapa_productos = {}
        self.mapa_promos = {}
        self.mapa_metodos = {}

        self._setup_ui()
        self.cargar_datos_iniciales()

    def _setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        
        self.panel_left = ctk.CTkFrame(self)
        self.panel_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        ctk.CTkLabel(self.panel_left, text="Nueva Venta", font=("Arial", 20, "bold")).pack(pady=10)

        self.combo_clientes = self._crear_combo("Cliente:")
        self.combo_empleados = self._crear_combo("Atendido por:")
        self.combo_pagos = self._crear_combo("Método de Pago:")
        
        ttk.Separator(self.panel_left).pack(fill="x", pady=10)

        self.combo_servicios = self._crear_seccion_seleccion("Servicios:", "servicio")
        self.combo_productos = self._crear_seccion_seleccion("Productos:", "producto")
        self.combo_promociones = self._crear_seccion_seleccion("Promociones:", "promo", color="#f39c12")

        self.entry_cantidad = ctk.CTkEntry(self.panel_left, placeholder_text="Cantidad")
        self.entry_cantidad.insert(0, "1")
        self.entry_cantidad.pack(pady=10)

        self.panel_right = ctk.CTkFrame(self)
        self.panel_right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        cols = ("Tipo", "Descripción", "Precio U.", "Cant.", "Subtotal")
        self.tree = ttk.Treeview(self.panel_right, columns=cols, show="headings")
        for col in cols: self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.lbl_total = ctk.CTkLabel(self.panel_right, text="TOTAL: 0.00", font=("Arial", 22, "bold"))
        self.lbl_total.pack(anchor="e", padx=20)

        ctk.CTkButton(self.panel_right, text="QUITAR ITEM", fg_color="#e74c3c", command=self.eliminar_item).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(self.panel_right, text="FINALIZAR VENTA", fg_color="#27ae60", command=self.procesar_venta_final).pack(side="right", padx=20, pady=10)

    def _crear_combo(self, titulo):
        ctk.CTkLabel(self.panel_left, text=titulo).pack(anchor="w", padx=10)
        combo = ctk.CTkComboBox(self.panel_left, width=250)
        combo.pack(pady=5)
        return combo

    def _crear_seccion_seleccion(self, titulo, tipo, color=None):
        ctk.CTkLabel(self.panel_left, text=titulo).pack(anchor="w", padx=10)
        combo = ctk.CTkComboBox(self.panel_left, width=250)
        combo.pack(pady=2)
        btn = ctk.CTkButton(self.panel_left, text=f"Agregar {tipo.capitalize()}", command=lambda: self.agregar_al_carrito(tipo))
        if color: btn.configure(fg_color=color)
        btn.pack(pady=5)
        return combo

    def cargar_datos_iniciales(self):
        clientes = db_conexion.ejecutar_consulta("SELECT cliente_id, nombre, apellido FROM Clientes", es_select=True)
        if clientes:
            self.mapa_clientes = {f"{c['nombre']} {c['apellido']}": c['cliente_id'] for c in clientes}
            self.combo_clientes.configure(values=list(self.mapa_clientes.keys()))

        empleados = db_conexion.ejecutar_consulta("SELECT empleado_id, nombre, apellido FROM Empleados", es_select=True)
        if empleados:
            self.mapa_empleados = {f"{e['nombre']} {e['apellido']}": e['empleado_id'] for e in empleados}
            self.combo_empleados.configure(values=list(self.mapa_empleados.keys()))

        metodos = db_conexion.ejecutar_consulta("SELECT metodo_pago_id, nombre_metodo FROM Metodo_Pago", es_select=True)
        if metodos:
            self.mapa_metodos = {m['nombre_metodo']: m['metodo_pago_id'] for m in metodos}
            self.combo_pagos.configure(values=list(self.mapa_metodos.keys()))

        servs = db_conexion.ejecutar_consulta("SELECT servicio_id, nombre_servicio, precio FROM Servicios", es_select=True)
        self.mapa_servicios = {s['nombre_servicio']: (s['servicio_id'], float(s['precio'])) for s in servs} if servs else {}
        self.combo_servicios.configure(values=list(self.mapa_servicios.keys()))

        prods = db_conexion.ejecutar_consulta("SELECT producto_id, nombre_producto, precio_venta FROM Productos", es_select=True)
        self.mapa_productos = {p['nombre_producto']: (p['producto_id'], float(p['precio_venta'])) for p in prods} if prods else {}
        self.combo_productos.configure(values=list(self.mapa_productos.keys()))

        promos = db_conexion.ejecutar_consulta("SELECT promocion_id, nombre_promocion, porcentaje_descuento FROM Promociones WHERE activo = 1", es_select=True)
        self.mapa_promos = {p['nombre_promocion']: (p['promocion_id'], float(p['porcentaje_descuento'])) for p in promos} if promos else {}
        self.combo_promociones.configure(values=list(self.mapa_promos.keys()))

    def agregar_al_carrito(self, tipo):
        cant_texto = self.entry_cantidad.get()
        cant = int(cant_texto) if cant_texto.isdigit() else 1
        
        if tipo == "servicio":
            nombre = self.combo_servicios.get()
            if nombre in self.mapa_servicios:
                item_id, precio_u = self.mapa_servicios[nombre]
                self._registrar_en_carrito("SERVICIO", item_id, nombre, precio_u, cant)
        
        elif tipo == "producto":
            nombre = self.combo_productos.get()
            if nombre in self.mapa_productos:
                item_id, precio_u = self.mapa_productos[nombre]
                self._registrar_en_carrito("PRODUCTO", item_id, nombre, precio_u, cant)

        elif tipo == "promo":
            nombre_p = self.combo_promociones.get()
            if nombre_p in self.mapa_promos:
                promo_id, porc = self.mapa_promos[nombre_p]

                query = """SELECT s.servicio_id, s.nombre_servicio, s.precio 
                           FROM Servicios s 
                           JOIN Promocion_Servicio ps ON s.servicio_id = ps.servicio_id 
                           WHERE ps.promocion_id = ?"""
                servs_promo = db_conexion.ejecutar_consulta(query, (promo_id,), es_select=True)
                
                for s in servs_promo:
                    precio_desc = float(s['precio']) * (1 - (porc / 100))
                    self._registrar_en_carrito("SERVICIO", s['servicio_id'], f"{s['nombre_servicio']} (Promo)", precio_desc, cant)

    def _registrar_en_carrito(self, tipo, item_id, nombre, precio_u, cant):
        self.carrito.append({
            "tipo": tipo, "id": item_id, "nombre": nombre, 
            "precio_u": precio_u, "cant": cant, "subtotal": precio_u * cant
        })
        self.actualizar_tabla()

    def eliminar_item(self):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            del self.carrito[idx]
            self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        total = sum(i['subtotal'] for i in self.carrito)
        for i in self.carrito:
            self.tree.insert("", "end", values=(i['tipo'], i['nombre'], f"{i['precio_u']:.2f}", i['cant'], f"{i['subtotal']:.2f}"))
        self.lbl_total.configure(text=f"TOTAL: {total:.2f}")

    def procesar_venta_final(self):
        if not self.carrito: return
        id_c = self.mapa_clientes.get(self.combo_clientes.get())
        id_e = self.mapa_empleados.get(self.combo_empleados.get())
        id_m = self.mapa_metodos.get(self.combo_pagos.get())
        total = sum(i['subtotal'] for i in self.carrito)

        if not all([id_c, id_e, id_m]):
            messagebox.showwarning("Faltan Datos", "Seleccione Cliente, Empleado y Método de Pago.")
            return

        conn = db_conexion.get_connection()
        try:
            cursor = conn.cursor()

            sql_v = "INSERT INTO Ventas (cliente_id, empleado_id, total_bruto, fecha_venta) VALUES (?, ?, ?, GETDATE())"
            cursor.execute(sql_v, (id_c, id_e, total))
            
            cursor.execute("SELECT @@IDENTITY")
            v_id = cursor.fetchone()[0]

            sql_d = """INSERT INTO Detalle_Venta (venta_id, servicio_id, producto_id, promocion_id, cantidad, precio_unitario, subtotal_linea) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            for i in self.carrito:
                cursor.execute(sql_d, (
                    v_id, 
                    i['id'] if i['tipo']=="SERVICIO" else None, 
                    i['id'] if i['tipo']=="PRODUCTO" else None, 
                    None, i['cant'], i['precio_u'], i['subtotal']
                ))

            sql_p = "INSERT INTO Pagos (venta_id, metodo_pago_id, monto_pagado, fecha_pago) VALUES (?, ?, ?, GETDATE())"
            cursor.execute(sql_p, (v_id, id_m, total))
            
            conn.commit()
            messagebox.showinfo("Éxito", "Venta guardada correctamente.")
            self.carrito = []
            self.actualizar_tabla()
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error SQL", f"No se pudo completar la transacción:\n{e}")
        finally:
            conn.close()