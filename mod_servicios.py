import customtkinter as ctk
from tkinter import ttk, messagebox
import db_conexion

class ServicioFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.id_servicio_seleccionado = None
        
        self.vars_categorias = {}     
        self.vars_especialidades = {}  

      
        ctk.CTkLabel(self, text="GESTIÓN DE SERVICIOS", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=10)

    
        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        
        self.tab_view = ctk.CTkTabview(self.frame_central, height=300)
        self.tab_view.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        self.tab_info = self.tab_view.add("Información")
        self.tab_cat = self.tab_view.add("Categorías")
        self.tab_esp = self.tab_view.add("Especialidades")

        self.entry_nombre = ctk.CTkEntry(self.tab_info, placeholder_text="Nombre del Servicio")
        self.entry_nombre.pack(pady=10, fill="x", padx=20)
        
        self.entry_desc = ctk.CTkEntry(self.tab_info, placeholder_text="Descripción breve")
        self.entry_desc.pack(pady=10, fill="x", padx=20)
        
        self.entry_precio = ctk.CTkEntry(self.tab_info, placeholder_text="Precio (Ej: 150.00)")
        self.entry_precio.pack(pady=10, fill="x", padx=20)
        
        self.entry_duracion = ctk.CTkEntry(self.tab_info, placeholder_text="Duración (minutos)")
        self.entry_duracion.pack(pady=10, fill="x", padx=20)

        self.scroll_cat = ctk.CTkScrollableFrame(self.tab_cat)
        self.scroll_cat.pack(fill="both", expand=True, padx=5, pady=5)

        self.scroll_esp = ctk.CTkScrollableFrame(self.tab_esp)
        self.scroll_esp.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_botones = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botones.pack(side="right", fill="y", padx=10, pady=20)

        ctk.CTkButton(self.frame_botones, text="Guardar", fg_color="green", command=self.guardar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Actualizar", fg_color="#1f538d", command=self.actualizar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Eliminar", fg_color="red", command=self.eliminar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Limpiar", fg_color="gray", command=self.limpiar).pack(pady=5, fill="x")

        cols = ("ID", "Servicio", "Precio", "Duración", "Descripción")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=40)
        self.tree.heading("Servicio", text="Servicio"); self.tree.column("Servicio", width=150)
        self.tree.heading("Precio", text="Precio"); self.tree.column("Precio", width=80)
        self.tree.heading("Duración", text="Mins"); self.tree.column("Duración", width=60)
        self.tree.heading("Descripción", text="Descripción"); self.tree.column("Descripción", width=250)

        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        self.cargar_catalogos()
        self.cargar_servicios()

    def cargar_catalogos(self):
        try:
            cats = db_conexion.ejecutar_consulta("SELECT categoria_id, nombre_categoria FROM Categorias_Servicio", es_select=True)
            for widget in self.scroll_cat.winfo_children(): widget.destroy()
            self.vars_categorias = {}
            if cats:
                for c in cats:
                    var = ctk.IntVar()
                    self.vars_categorias[c['categoria_id']] = var
                    ctk.CTkCheckBox(self.scroll_cat, text=c['nombre_categoria'], variable=var).pack(anchor="w", pady=2)

            esps = db_conexion.ejecutar_consulta("SELECT especialidad_id, nombre_especialidad FROM Especialidades", es_select=True)
            for widget in self.scroll_esp.winfo_children(): widget.destroy()
            self.vars_especialidades = {}
            if esps:
                for e in esps:
                    var = ctk.IntVar()
                    self.vars_especialidades[e['especialidad_id']] = var
                    ctk.CTkCheckBox(self.scroll_esp, text=e['nombre_especialidad'], variable=var).pack(anchor="w", pady=2)
        except Exception as e:
            print(f"Error catálogos: {e}")

    def cargar_servicios(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        sql = "SELECT servicio_id, nombre_servicio, precio, duracion_minutos, descripcion FROM Servicios"
        filas = db_conexion.ejecutar_consulta(sql, es_select=True)
        if filas:
            for f in filas:
                self.tree.insert("", "end", values=(f['servicio_id'], f['nombre_servicio'], f['precio'], f['duracion_minutos'], f['descripcion']))

    def guardar(self):
        nom = self.entry_nombre.get().strip()
        prec = self.entry_precio.get().strip()
        dur = self.entry_duracion.get().strip()
        if not nom or not prec or not dur:
            messagebox.showwarning("Faltan datos", "Nombre, Precio y Duración son obligatorios.")
            return

        conn, cursor = db_conexion.conectar()
        try:
            sql = "INSERT INTO Servicios (nombre_servicio, descripcion, precio, duracion_minutos) OUTPUT INSERTED.servicio_id VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (nom, self.entry_desc.get(), prec, dur))
            sid = cursor.fetchone()[0]
            self._guardar_relaciones(cursor, sid)
            conn.commit()
            messagebox.showinfo("Éxito", "Servicio guardado.")
            self.limpiar(); self.cargar_servicios()
        except Exception as e:
            conn.rollback(); messagebox.showerror("Error", str(e))
        finally: conn.close()

    def actualizar(self):
        if not self.id_servicio_seleccionado: return
        conn, cursor = db_conexion.conectar()
        try:
            cursor.execute("UPDATE Servicios SET nombre_servicio=?, descripcion=?, precio=?, duracion_minutos=? WHERE servicio_id=?",
                           (self.entry_nombre.get(), self.entry_desc.get(), self.entry_precio.get(), self.entry_duracion.get(), self.id_servicio_seleccionado))
            cursor.execute("DELETE FROM Servicio_Categoria WHERE servicio_id=?", (self.id_servicio_seleccionado,))
            cursor.execute("DELETE FROM Servicio_Especialidad WHERE servicio_id=?", (self.id_servicio_seleccionado,))
            self._guardar_relaciones(cursor, self.id_servicio_seleccionado)
            conn.commit()
            messagebox.showinfo("Éxito", "Servicio actualizado."); self.limpiar(); self.cargar_servicios()
        except Exception as e:
            conn.rollback(); messagebox.showerror("Error", str(e))
        finally: conn.close()

    def _guardar_relaciones(self, cursor, sid):
        for cat_id, var in self.vars_categorias.items():
            if var.get(): cursor.execute("INSERT INTO Servicio_Categoria VALUES (?, ?)", (sid, cat_id))
        for esp_id, var in self.vars_especialidades.items():
            if var.get(): cursor.execute("INSERT INTO Servicio_Especialidad VALUES (?, ?)", (sid, esp_id))

    def eliminar(self):
        if not self.id_servicio_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un servicio de la tabla.")
            return
            
        if messagebox.askyesno("Confirmar", "¿Eliminar este servicio permanentemente?"):
            conn, cursor = db_conexion.conectar()
            try:
                
                cursor.execute("DELETE FROM Servicio_Categoria WHERE servicio_id=?", (self.id_servicio_seleccionado,))
                cursor.execute("DELETE FROM Servicio_Especialidad WHERE servicio_id=?", (self.id_servicio_seleccionado,))
                
                cursor.execute("DELETE FROM Servicios WHERE servicio_id=?", (self.id_servicio_seleccionado,))
                conn.commit()
                messagebox.showinfo("Éxito", "Servicio eliminado.")
                self.limpiar(); self.cargar_servicios()
            except Exception as e:
                conn.rollback()
                if "REFERENCE constraint" in str(e):
                    messagebox.showerror("Error de Integridad", 
                        "No se puede eliminar este servicio porque ya ha sido utilizado en CITAS o VENTAS.\n\n"
                        "Considere solo actualizar su descripción o precio.")
                else:
                    messagebox.showerror("Error", str(e))
            finally: conn.close()

    def seleccionar(self, event):
        item = self.tree.focus()
        if not item: return
        vals = self.tree.item(item, 'values')
        self.id_servicio_seleccionado = vals[0]
        self.entry_nombre.delete(0, "end"); self.entry_nombre.insert(0, vals[1])
        self.entry_precio.delete(0, "end"); self.entry_precio.insert(0, vals[2])
        self.entry_duracion.delete(0, "end"); self.entry_duracion.insert(0, vals[3])
        self.entry_desc.delete(0, "end")
        if vals[4] and vals[4] != 'None': self.entry_desc.insert(0, vals[4])

        for v in self.vars_categorias.values(): v.set(0)
        for v in self.vars_especialidades.values(): v.set(0)

        cats = db_conexion.ejecutar_consulta("SELECT categoria_id FROM Servicio_Categoria WHERE servicio_id=?", (self.id_servicio_seleccionado,), es_select=True)
        for c in (cats or []):
            if c['categoria_id'] in self.vars_categorias: self.vars_categorias[c['categoria_id']].set(1)
        
        esps = db_conexion.ejecutar_consulta("SELECT especialidad_id FROM Servicio_Especialidad WHERE servicio_id=?", (self.id_servicio_seleccionado,), es_select=True)
        for e in (esps or []):
            if e['especialidad_id'] in self.vars_especialidades: self.vars_especialidades[e['especialidad_id']].set(1)

    def limpiar(self):
        self.id_servicio_seleccionado = None
        self.entry_nombre.delete(0, "end"); self.entry_desc.delete(0, "end")
        self.entry_precio.delete(0, "end"); self.entry_duracion.delete(0, "end")
        for v in self.vars_categorias.values(): v.set(0)
        for v in self.vars_especialidades.values(): v.set(0)