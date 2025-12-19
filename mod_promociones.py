import customtkinter as ctk
from tkinter import ttk, messagebox
import db_conexion
from datetime import date, datetime

class PromocionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.id_promo = None
        self.vars_servicios = {} 

        ctk.CTkLabel(self, text="GESTIÓN DE PROMOCIONES", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=10)

        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)

        self.tab_view = ctk.CTkTabview(self.frame_central, width=700, height=350)
        self.tab_view.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tab_datos = self.tab_view.add("Datos Generales")
        self.tab_servs = self.tab_view.add("Servicios Incluidos")

        self.entry_nombre = ctk.CTkEntry(self.tab_datos, placeholder_text="Nombre Promoción (Ej: Verano 2024)")
        self.entry_nombre.pack(pady=10, fill="x", padx=20)

        self.entry_desc = ctk.CTkEntry(self.tab_datos, placeholder_text="Descripción breve")
        self.entry_desc.pack(pady=10, fill="x", padx=20)

        frame_fechas = ctk.CTkFrame(self.tab_datos, fg_color="transparent")
        frame_fechas.pack(fill="x", padx=20, pady=10)
        
        self.entry_inicio = ctk.CTkEntry(frame_fechas, placeholder_text="Inicio (YYYY-MM-DD)")
        self.entry_inicio.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.entry_fin = ctk.CTkEntry(frame_fechas, placeholder_text="Fin (YYYY-MM-DD)")
        self.entry_fin.pack(side="right", fill="x", expand=True, padx=(5, 0))

        frame_desc = ctk.CTkFrame(self.tab_datos, fg_color="transparent")
        frame_desc.pack(fill="x", padx=20, pady=10)

        self.entry_porcentaje = ctk.CTkEntry(frame_desc, placeholder_text="% Descuento (Opcional)", width=150)
        self.entry_porcentaje.pack(side="left")
        
        self.switch_activo = ctk.CTkSwitch(frame_desc, text="Promoción Activa")
        self.switch_activo.select() 
        self.switch_activo.pack(side="left", padx=20)

        ctk.CTkLabel(self.tab_servs, text="Selecciona los servicios que aplican:", text_color="gray").pack(pady=5)
        self.scroll_servs = ctk.CTkScrollableFrame(self.tab_servs)
        self.scroll_servs.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_botones = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botones.pack(side="right", fill="y", padx=10, pady=20)

        ctk.CTkButton(self.frame_botones, text="Guardar", fg_color="green", command=self.guardar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Actualizar", fg_color="#1f538d", command=self.actualizar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Eliminar", fg_color="red", command=self.eliminar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Limpiar", fg_color="gray", command=self.limpiar).pack(pady=5, fill="x")

        cols = ("ID", "Nombre", "Inicio", "Fin", "Desc %", "Estado")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        self.tree.column("ID", width=40)
        self.tree.column("Nombre", width=200)
        self.tree.column("Inicio", width=100)
        self.tree.column("Fin", width=100)
        self.tree.column("Desc %", width=80)
        self.tree.column("Estado", width=80)
        
        for c in cols: self.tree.heading(c, text=c)
        
        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        self.cargar_servicios_ui()
        self.cargar_tabla()

    def cargar_servicios_ui(self):
        for w in self.scroll_servs.winfo_children(): w.destroy()
        self.vars_servicios = {}
        
        servs = db_conexion.ejecutar_consulta("SELECT servicio_id, nombre_servicio FROM Servicios", es_select=True)
        if servs:
            for s in servs:
                var = ctk.IntVar()
                self.vars_servicios[s['servicio_id']] = var
                ctk.CTkCheckBox(self.scroll_servs, text=s['nombre_servicio'], variable=var).pack(anchor="w", pady=2)

    def cargar_tabla(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        sql = "SELECT promocion_id, nombre_promocion, fecha_inicio, fecha_fin, porcentaje_descuento, activo FROM Promociones"
        datos = db_conexion.ejecutar_consulta(sql, es_select=True)
        if datos:
            for d in datos:
                estado = "ACTIVO" if d['activo'] else "Inactivo"
                desc_text = f"{d['porcentaje_descuento']}%" if d['porcentaje_descuento'] else "0%"
                self.tree.insert("", "end", values=(
                    d['promocion_id'], d['nombre_promocion'], 
                    d['fecha_inicio'], d['fecha_fin'], 
                    desc_text, estado
                ))

    def _guardar_relaciones(self, cursor, promocion_id):
        sql_rel = "INSERT INTO Promocion_Servicio (promocion_id, servicio_id) VALUES (?, ?)"
        for servicio_id, variable in self.vars_servicios.items():
            if variable.get() == 1:
                cursor.execute(sql_rel, (promocion_id, servicio_id))

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        f_ini = self.entry_inicio.get()
        f_fin = self.entry_fin.get()
        porc = self.entry_porcentaje.get().strip()
        activo = 1 if self.switch_activo.get() == 1 else 0

        if not nombre or not f_ini or not f_fin:
            messagebox.showwarning("Datos", "Nombre y fechas son obligatorios")
            return

        sql_check = "SELECT COUNT(*) as total FROM Promociones WHERE nombre_promocion = ?"
        existe = db_conexion.ejecutar_consulta(sql_check, (nombre,), es_select=True)
        if existe and existe[0]['total'] > 0:
            messagebox.showerror("Error", f"Ya existe la promoción '{nombre}'.")
            return

        try:
            porc_val = float(porc) if porc != "" else 0.0
            if porc_val < 0 or porc_val > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El porcentaje debe ser un número entre 0 y 100")
            return

        try:
            inicio_date = datetime.strptime(f_ini, "%Y-%m-%d").date()
            fin_date = datetime.strptime(f_fin, "%Y-%m-%d").date()
            if fin_date < inicio_date:
                messagebox.showerror("Error", "La fecha de fin no puede ser menor a la de inicio.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido (YYYY-MM-DD)")
            return

        conn, cursor = db_conexion.conectar()
        try:
            sql = """
            INSERT INTO Promociones (nombre_promocion, descripcion, fecha_inicio, fecha_fin, porcentaje_descuento, activo)
            OUTPUT INSERTED.promocion_id
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (nombre, self.entry_desc.get(), inicio_date, fin_date, porc_val, activo))
            pid = cursor.fetchone()[0]
            self._guardar_relaciones(cursor, pid)
            conn.commit()
            messagebox.showinfo("Éxito", "Promoción creada")
            self.limpiar(); self.cargar_tabla()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            conn.close()

    def actualizar(self):
        if not self.id_promo:
            messagebox.showwarning("Error", "Seleccione una promoción")
            return

        nombre = self.entry_nombre.get().strip()
        f_ini = self.entry_inicio.get()
        f_fin = self.entry_fin.get()
        porc = self.entry_porcentaje.get().strip()
        activo = 1 if self.switch_activo.get() == 1 else 0

        try:
            porc_val = float(porc) if porc != "" else 0.0
            if porc_val < 0 or porc_val > 100: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Porcentaje inválido")
            return

        try:
            inicio_date = datetime.strptime(f_ini, "%Y-%m-%d").date()
            fin_date = datetime.strptime(f_fin, "%Y-%m-%d").date()
        except:
            messagebox.showerror("Error", "Fecha inválida"); return

        conn, cursor = db_conexion.conectar()
        try:
            sql = """
            UPDATE Promociones
            SET nombre_promocion=?, descripcion=?, fecha_inicio=?, fecha_fin=?, porcentaje_descuento=?, activo=?
            WHERE promocion_id=?
            """
            cursor.execute(sql, (nombre, self.entry_desc.get(), inicio_date, fin_date, porc_val, activo, self.id_promo))
            cursor.execute("DELETE FROM Promocion_Servicio WHERE promocion_id=?", (self.id_promo,))
            self._guardar_relaciones(cursor, self.id_promo)
            conn.commit()
            messagebox.showinfo("Éxito", "Promoción actualizada")
            self.limpiar(); self.cargar_tabla()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def seleccionar(self, event):
        item = self.tree.focus()
        if not item: return
        vals = self.tree.item(item, 'values')
        self.id_promo = vals[0]
        
        datos = db_conexion.ejecutar_consulta("SELECT * FROM Promociones WHERE promocion_id=?", (self.id_promo,), es_select=True)
        if datos:
            d = datos[0]
            self.entry_nombre.delete(0, "end"); self.entry_nombre.insert(0, d['nombre_promocion'])
            self.entry_desc.delete(0, "end"); self.entry_desc.insert(0, d['descripcion'] or "")
            self.entry_inicio.delete(0, "end"); self.entry_inicio.insert(0, str(d['fecha_inicio']))
            self.entry_fin.delete(0, "end"); self.entry_fin.insert(0, str(d['fecha_fin']))
            self.entry_porcentaje.delete(0, "end")
            # Insertar valor del porcentaje (si es 0, aparecerá 0)
            self.entry_porcentaje.insert(0, str(d['porcentaje_descuento']))
            
            if d['activo']: self.switch_activo.select()
            else: self.switch_activo.deselect()

        for v in self.vars_servicios.values(): v.set(0)
        rels = db_conexion.ejecutar_consulta("SELECT servicio_id FROM Promocion_Servicio WHERE promocion_id=?", (self.id_promo,), es_select=True)
        if rels:
            for r in rels:
                if r['servicio_id'] in self.vars_servicios:
                    self.vars_servicios[r['servicio_id']].set(1)

    def eliminar(self):
        if self.id_promo:
            if messagebox.askyesno("Confirmar", "¿Eliminar Promoción?"):
                if db_conexion.ejecutar_consulta("DELETE FROM Promociones WHERE promocion_id=?", (self.id_promo,)):
                    self.limpiar(); self.cargar_tabla()

    def limpiar(self):
        self.id_promo = None
        self.entry_nombre.delete(0, "end")
        self.entry_desc.delete(0, "end")
        self.entry_inicio.delete(0, "end")
        self.entry_fin.delete(0, "end")
        self.entry_porcentaje.delete(0, "end")
        self.switch_activo.select()
        for v in self.vars_servicios.values(): v.set(0)
        self.cargar_servicios_ui()