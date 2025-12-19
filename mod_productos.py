import customtkinter as ctk
from tkinter import ttk, messagebox
import db_conexion
from datetime import datetime

class ProductoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.map_proveedores = {} 
        self.map_productos = {}   
        self.map_empleados = {}   
        self.id_producto_selec = None
        self.id_proveedor_selec = None

        ctk.CTkLabel(self, text="GESTIÓN DE INVENTARIO Y PRODUCTOS", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=10)

        self.tab_view = ctk.CTkTabview(self, width=800, height=500)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)

        self.tab_prods = self.tab_view.add("Productos")
        self.tab_movs = self.tab_view.add("Control de Stock")
        self.tab_provs = self.tab_view.add("Proveedores")


        frame_p_form = ctk.CTkFrame(self.tab_prods, fg_color="transparent")
        frame_p_form.pack(fill="x", padx=10, pady=5)


        self.entry_nom_prod = ctk.CTkEntry(frame_p_form, placeholder_text="Nombre Producto")
        self.entry_nom_prod.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.entry_desc_prod = ctk.CTkEntry(frame_p_form, placeholder_text="Descripción")
        self.entry_desc_prod.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.entry_precio = ctk.CTkEntry(frame_p_form, placeholder_text="Precio Venta")
        self.entry_precio.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.combo_prov_prod = ctk.CTkComboBox(frame_p_form, values=["Seleccione Proveedor"])
        self.combo_prov_prod.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        frame_p_btns = ctk.CTkFrame(self.tab_prods, fg_color="transparent")
        frame_p_btns.pack(fill="x", padx=10)
        ctk.CTkButton(frame_p_btns, text="Guardar Nuevo", fg_color="green", command=self.guardar_producto).pack(side="left", padx=5)
        ctk.CTkButton(frame_p_btns, text="Actualizar Datos", fg_color="#1f538d", command=self.actualizar_producto).pack(side="left", padx=5)
        ctk.CTkButton(frame_p_btns, text="Limpiar", fg_color="gray", command=self.limpiar_producto).pack(side="left", padx=5)

        self.tree_prod = ttk.Treeview(self.tab_prods, columns=("ID", "Producto", "Proveedor", "Precio", "Stock"), show="headings", height=10)
        self.tree_prod.heading("ID", text="ID"); self.tree_prod.column("ID", width=30)
        self.tree_prod.heading("Producto", text="Producto"); self.tree_prod.column("Producto", width=200)
        self.tree_prod.heading("Proveedor", text="Proveedor"); self.tree_prod.column("Proveedor", width=150)
        self.tree_prod.heading("Precio", text="Precio"); self.tree_prod.column("Precio", width=80)
        self.tree_prod.heading("Stock", text="Stock"); self.tree_prod.column("Stock", width=60)
        self.tree_prod.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_prod.bind("<<TreeviewSelect>>", self.seleccionar_producto)


        frame_m_form = ctk.CTkFrame(self.tab_movs)
        frame_m_form.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_m_form, text="Registrar Movimiento de Stock", font=("Arial", 14, "bold")).pack(pady=5)
        
        frame_grid_mov = ctk.CTkFrame(frame_m_form, fg_color="transparent")
        frame_grid_mov.pack(fill="x", padx=10, pady=5)

        self.combo_mov_prod = ctk.CTkComboBox(frame_grid_mov, width=200, values=["Seleccione Producto"])
        self.combo_mov_prod.grid(row=0, column=0, padx=10, pady=5)
        
        self.combo_tipo_mov = ctk.CTkComboBox(frame_grid_mov, values=["ENTRADA", "SALIDA", "AJUSTE"])
        self.combo_tipo_mov.grid(row=0, column=1, padx=10, pady=5)

        self.entry_cantidad = ctk.CTkEntry(frame_grid_mov, placeholder_text="Cantidad")
        self.entry_cantidad.grid(row=0, column=2, padx=10, pady=5)

        self.combo_mov_emp = ctk.CTkComboBox(frame_grid_mov, values=["Empleado Responsable"])
        self.combo_mov_emp.grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkButton(frame_m_form, text="REGISTRAR MOVIMIENTO", fg_color="#d84315", command=self.registrar_movimiento).pack(pady=10, fill="x", padx=50)

 
        ctk.CTkLabel(self.tab_movs, text="Historial Reciente").pack(anchor="w", padx=10)
        self.tree_mov = ttk.Treeview(self.tab_movs, columns=("Fecha", "Producto", "Tipo", "Cant", "Resp"), show="headings")
        self.tree_mov.heading("Fecha", text="Fecha"); self.tree_mov.column("Fecha", width=120)
        self.tree_mov.heading("Producto", text="Producto"); self.tree_mov.column("Producto", width=200)
        self.tree_mov.heading("Tipo", text="Tipo"); self.tree_mov.column("Tipo", width=80)
        self.tree_mov.heading("Cant", text="Cant"); self.tree_mov.column("Cant", width=50)
        self.tree_mov.heading("Resp", text="Responsable"); self.tree_mov.column("Resp", width=150)
        self.tree_mov.pack(fill="both", expand=True, padx=10, pady=10)


        frame_prov_form = ctk.CTkFrame(self.tab_provs, fg_color="transparent")
        frame_prov_form.pack(fill="x", padx=10, pady=10)

        self.entry_prov_nom = ctk.CTkEntry(frame_prov_form, placeholder_text="Nombre Empresa")
        self.entry_prov_nom.pack(side="left", fill="x", expand=True, padx=5)
        
        self.entry_prov_cont = ctk.CTkEntry(frame_prov_form, placeholder_text="Nombre Contacto")
        self.entry_prov_cont.pack(side="left", fill="x", expand=True, padx=5)

        self.entry_prov_tel = ctk.CTkEntry(frame_prov_form, placeholder_text="Teléfono")
        self.entry_prov_tel.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkButton(frame_prov_form, text="Guardar", width=80, command=self.guardar_proveedor).pack(side="left", padx=5)
        ctk.CTkButton(frame_prov_form, text="Eliminar", width=80, fg_color="red", command=self.eliminar_proveedor).pack(side="left", padx=5)

        self.tree_prov = ttk.Treeview(self.tab_provs, columns=("ID", "Empresa", "Contacto", "Tel"), show="headings")
        for c in ("ID", "Empresa", "Contacto", "Tel"): self.tree_prov.heading(c, text=c)
        self.tree_prov.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_prov.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

        self.cargar_combos()
        self.cargar_tablas_todas()

    def guardar_proveedor(self):
        nom = self.entry_prov_nom.get()
        cont = self.entry_prov_cont.get()
        tel = self.entry_prov_tel.get()
        
        if not nom: return
        
        if db_conexion.ejecutar_consulta("INSERT INTO Proveedores (nombre_proveedor, contacto, telefono) VALUES (?,?,?)", (nom, cont, tel)):
            messagebox.showinfo("Éxito", "Proveedor Guardado")
            self.limpiar_prov()
            self.cargar_combos()
            self.cargar_tablas_todas()

    def eliminar_proveedor(self):
        if self.id_proveedor_selec:
            if messagebox.askyesno("Borrar", "¿Eliminar proveedor?"):
                db_conexion.ejecutar_consulta("DELETE FROM Proveedores WHERE proveedor_id=?", (self.id_proveedor_selec,))
                self.limpiar_prov()
                self.cargar_tablas_todas()

    def seleccionar_proveedor(self, event):
        item = self.tree_prov.focus()
        if not item: return
        val = self.tree_prov.item(item, 'values')
        self.id_proveedor_selec = val[0]
        self.entry_prov_nom.delete(0, "end"); self.entry_prov_nom.insert(0, val[1])
        self.entry_prov_cont.delete(0, "end"); self.entry_prov_cont.insert(0, val[2])
        self.entry_prov_tel.delete(0, "end"); self.entry_prov_tel.insert(0, val[3])

    def limpiar_prov(self):
        self.id_proveedor_selec = None
        self.entry_prov_nom.delete(0, "end")
        self.entry_prov_cont.delete(0, "end")
        self.entry_prov_tel.delete(0, "end")

    def guardar_producto(self):
        nom = self.entry_nom_prod.get()
        desc = self.entry_desc_prod.get()
        prec = self.entry_precio.get()
        prov_txt = self.combo_prov_prod.get()

        if not nom or not prec or prov_txt not in self.map_proveedores:
            messagebox.showwarning("Error", "Revise Nombre, Precio y Seleccione un Proveedor válido")
            return

        pid = self.map_proveedores[prov_txt]
        
        try:
            db_conexion.ejecutar_consulta("INSERT INTO Productos (nombre_producto, descripcion, proveedor_id, precio_venta, stock_actual) VALUES (?,?,?,?,0)", 
                                          (nom, desc, pid, float(prec)))
            messagebox.showinfo("Éxito", "Producto Creado (Stock inicial 0)")
            self.limpiar_producto()
            self.cargar_tablas_todas()
            self.cargar_combos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_producto(self):
        if not self.id_producto_selec: return
        nom = self.entry_nom_prod.get()
        desc = self.entry_desc_prod.get()
        prec = self.entry_precio.get()
        prov_txt = self.combo_prov_prod.get()
        
        if prov_txt not in self.map_proveedores: return
        pid = self.map_proveedores[prov_txt]

        sql = "UPDATE Productos SET nombre_producto=?, descripcion=?, proveedor_id=?, precio_venta=? WHERE producto_id=?"
        if db_conexion.ejecutar_consulta(sql, (nom, desc, pid, float(prec), self.id_producto_selec)):
            messagebox.showinfo("Éxito", "Producto Actualizado")
            self.limpiar_producto()
            self.cargar_tablas_todas()

    def seleccionar_producto(self, event):
        item = self.tree_prod.focus()
        if not item: return
        val = self.tree_prod.item(item, 'values')
        self.id_producto_selec = val[0]
        
        self.entry_nom_prod.delete(0, "end"); self.entry_nom_prod.insert(0, val[1])
        self.combo_prov_prod.set(val[2])
        self.entry_precio.delete(0, "end"); self.entry_precio.insert(0, val[3])

    def limpiar_producto(self):
        self.id_producto_selec = None
        self.entry_nom_prod.delete(0, "end")
        self.entry_desc_prod.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.combo_prov_prod.set("")

    def registrar_movimiento(self):
        prod_txt = self.combo_mov_prod.get()
        tipo = self.combo_tipo_mov.get()
        cant = self.entry_cantidad.get()
        emp_txt = self.combo_mov_emp.get()

        if prod_txt not in self.map_productos or emp_txt not in self.map_empleados:
            messagebox.showerror("Error", "Seleccione Producto y Empleado válidos")
            return
        
        if not cant.isdigit() or int(cant) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return

        prod_id = self.map_productos[prod_txt]
        emp_id = self.map_empleados[emp_txt]
        cantidad = int(cant)

        conn, cursor = db_conexion.conectar()
        try:
            sql_mov = "INSERT INTO Movimiento_Inventario (producto_id, tipo_movimiento, cantidad, empleado_id) VALUES (?,?,?,?)"
            cursor.execute(sql_mov, (prod_id, tipo, cantidad, emp_id))

            if tipo == "ENTRADA":
                sql_upd = "UPDATE Productos SET stock_actual = stock_actual + ? WHERE producto_id = ?"
                cursor.execute(sql_upd, (cantidad, prod_id))
            elif tipo == "SALIDA":
                cursor.execute("SELECT stock_actual FROM Productos WHERE producto_id = ?", (prod_id,))
                stock_actual = cursor.fetchone()[0]
                if stock_actual < cantidad:
                    raise Exception(f"Stock insuficiente. Tienes {stock_actual}, intentas sacar {cantidad}.")
                
                sql_upd = "UPDATE Productos SET stock_actual = stock_actual - ? WHERE producto_id = ?"
                cursor.execute(sql_upd, (cantidad, prod_id))
            
            elif tipo == "AJUSTE":
                sql_upd = "UPDATE Productos SET stock_actual = stock_actual + ? WHERE producto_id = ?"
                cursor.execute(sql_upd, (cantidad, prod_id))

            conn.commit()
            messagebox.showinfo("Éxito", "Movimiento Registrado")
            self.entry_cantidad.delete(0, "end")
            self.cargar_tablas_todas() 
            self.cargar_movimientos_tabla() 

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error Transacción", str(e))
        finally:
            conn.close()


    def cargar_combos(self):

        provs = db_conexion.ejecutar_consulta("SELECT proveedor_id, nombre_proveedor FROM Proveedores", es_select=True)
        self.map_proveedores = {p['nombre_proveedor']: p['proveedor_id'] for p in provs} if provs else {}
        self.combo_prov_prod.configure(values=list(self.map_proveedores.keys()))

        prods = db_conexion.ejecutar_consulta("SELECT producto_id, nombre_producto FROM Productos", es_select=True)
        self.map_productos = {p['nombre_producto']: p['producto_id'] for p in prods} if prods else {}
        self.combo_mov_prod.configure(values=list(self.map_productos.keys()))

        emps = db_conexion.ejecutar_consulta("SELECT empleado_id, nombre, apellido FROM Empleados", es_select=True)
        self.map_empleados = {f"{e['nombre']} {e['apellido']}": e['empleado_id'] for e in emps} if emps else {}
        self.combo_mov_emp.configure(values=list(self.map_empleados.keys()))

    def cargar_tablas_todas(self):

        for i in self.tree_prov.get_children(): self.tree_prov.delete(i)
        provs = db_conexion.ejecutar_consulta("SELECT * FROM Proveedores", es_select=True)
        if provs:
            for p in provs: 
                self.tree_prov.insert("", "end", values=(
                    p['proveedor_id'], 
                    p['nombre_proveedor'], 
                    p['contacto'], 
                    p['telefono']
                ))

        for i in self.tree_prod.get_children(): self.tree_prod.delete(i)
        sql = """SELECT p.producto_id, p.nombre_producto, pv.nombre_proveedor, p.precio_venta, p.stock_actual 
                 FROM Productos p JOIN Proveedores pv ON p.proveedor_id = pv.proveedor_id"""
        prods = db_conexion.ejecutar_consulta(sql, es_select=True)
        if prods:
            for p in prods: 

                self.tree_prod.insert("", "end", values=(
                    p['producto_id'], 
                    p['nombre_producto'], 
                    p['nombre_proveedor'], 
                    p['precio_venta'], 
                    p['stock_actual']
                ))
            
        self.cargar_movimientos_tabla()

    def cargar_movimientos_tabla(self):
        for i in self.tree_mov.get_children(): self.tree_mov.delete(i)
        sql = """SELECT m.fecha_movimiento, p.nombre_producto, m.tipo_movimiento, m.cantidad, e.nombre
                 FROM Movimiento_Inventario m
                 JOIN Productos p ON m.producto_id = p.producto_id
                 LEFT JOIN Empleados e ON m.empleado_id = e.empleado_id
                 ORDER BY m.fecha_movimiento DESC"""
        movs = db_conexion.ejecutar_consulta(sql, es_select=True)
        if movs:
            for m in movs:
                
                dt = m['fecha_movimiento']
                fecha = dt.strftime("%Y-%m-%d %H:%M")
                
                self.tree_mov.insert("", "end", values=(
                    fecha, 
                    m['nombre_producto'], 
                    m['tipo_movimiento'], 
                    m['cantidad'], 
                    m['nombre']
                ))