import customtkinter as ctk
from tkinter import ttk, messagebox
import db_conexion

class EmpleadoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.mapa_roles = {}
        self.vars_especialidades = {} 
        self.controles_horario = []
        self.id_empleado_seleccionado = None

        ctk.CTkLabel(self, text="GESTIÓN DE PERSONAL Y HORARIOS", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=10)

        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)

        self.tab_view = ctk.CTkTabview(self.frame_central, width=700, height=400)
        self.tab_view.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.tab_datos = self.tab_view.add("Datos")
        self.tab_esp = self.tab_view.add("Especialidades")
        self.tab_horario = self.tab_view.add("Horarios")

        # Pestaña Datos
        self.entry_nombre = ctk.CTkEntry(self.tab_datos, placeholder_text="Nombre")
        self.entry_nombre.pack(pady=5, fill="x", padx=20)
        self.entry_apellido = ctk.CTkEntry(self.tab_datos, placeholder_text="Apellido")
        self.entry_apellido.pack(pady=5, fill="x", padx=20)
        self.entry_telefono = ctk.CTkEntry(self.tab_datos, placeholder_text="Teléfono")
        self.entry_telefono.pack(pady=5, fill="x", padx=20)
        self.entry_email = ctk.CTkEntry(self.tab_datos, placeholder_text="Email")
        self.entry_email.pack(pady=5, fill="x", padx=20)
        
        ctk.CTkLabel(self.tab_datos, text="Rol:").pack(anchor="w", padx=20)
        self.cbo_rol = ctk.CTkComboBox(self.tab_datos, state="readonly")
        self.cbo_rol.pack(pady=5, fill="x", padx=20)
        
        self.var_activo = ctk.IntVar(value=1)
        ctk.CTkCheckBox(self.tab_datos, text="Empleado Activo", variable=self.var_activo).pack(pady=10, padx=20, anchor="w")

        self.scroll_esp = ctk.CTkScrollableFrame(self.tab_esp)
        self.scroll_esp.pack(fill="both", expand=True, padx=5, pady=5)

        self.crear_controles_horario()

        self.frame_botones = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botones.pack(side="right", fill="y", padx=10, pady=20)

        ctk.CTkButton(self.frame_botones, text="Guardar Nuevo", fg_color="green", command=self.guardar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Actualizar", fg_color="#1f538d", command=self.actualizar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Eliminar / Baja", fg_color="red", command=self.eliminar).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Limpiar Campos", fg_color="gray", command=self.limpiar).pack(pady=5, fill="x")

        cols = ("ID", "Nombre", "Apellido", "Rol", "Teléfono")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=6)
        for c in cols: 
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        self.cargar_maestros()
        self.cargar_empleados()

    def crear_controles_horario(self):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        scroll = ctk.CTkScrollableFrame(self.tab_horario)
        scroll.pack(fill="both", expand=True)
        for i, dia in enumerate(dias):
            f = ctk.CTkFrame(scroll, fg_color="transparent")
            f.pack(fill="x", pady=2)
            var = ctk.IntVar()
            ctk.CTkCheckBox(f, text=dia, variable=var, width=120).pack(side="left")
            ini = ctk.CTkEntry(f, width=80, placeholder_text="09:00"); ini.pack(side="left", padx=5)
            fin = ctk.CTkEntry(f, width=80, placeholder_text="18:00"); fin.pack(side="left", padx=5)
            self.controles_horario.append({"dia": i+1, "chk": var, "ini": ini, "fin": fin})

    def cargar_maestros(self):
        try:
            roles = db_conexion.ejecutar_consulta("SELECT rol_id, nombre_rol FROM Roles_Empleado", es_select=True)
            self.mapa_roles = {r['nombre_rol']: r['rol_id'] for r in roles} if roles else {}
            self.cbo_rol.configure(values=list(self.mapa_roles.keys()))
            
            for widget in self.scroll_esp.winfo_children(): widget.destroy()
            self.vars_especialidades = {}
            esps = db_conexion.ejecutar_consulta("SELECT especialidad_id, nombre_especialidad FROM Especialidades", es_select=True)
            if esps:
                for e in esps:
                    var = ctk.IntVar()
                    self.vars_especialidades[e['especialidad_id']] = var
                    ctk.CTkCheckBox(self.scroll_esp, text=e['nombre_especialidad'], variable=var).pack(anchor="w", pady=2)
        except Exception as e: print(f"Error maestros: {e}")

    def cargar_empleados(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        sql = "SELECT e.empleado_id, e.nombre, e.apellido, r.nombre_rol, e.telefono FROM Empleados e JOIN Roles_Empleado r ON e.rol_id=r.rol_id"
        datos = db_conexion.ejecutar_consulta(sql, es_select=True)
        if datos:
            for d in datos:
                self.tree.insert("", "end", values=(d['empleado_id'], d['nombre'], d['apellido'], d['nombre_rol'], d['telefono']))

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        rol_id = self.mapa_roles.get(self.cbo_rol.get())
        if not nombre or not email:
            messagebox.showwarning("Faltan datos", "Nombre y Email son obligatorios.")
            return
        conn, cursor = db_conexion.conectar()
        try:
            sql = "INSERT INTO Empleados (nombre, apellido, telefono, email, rol_id, activo) OUTPUT INSERTED.empleado_id VALUES (?,?,?,?,?,?)"
            cursor.execute(sql, (nombre, self.entry_apellido.get(), self.entry_telefono.get(), email, rol_id, self.var_activo.get()))
            eid = cursor.fetchone()[0]
            self._guardar_detalles(cursor, eid)
            conn.commit()
            messagebox.showinfo("Éxito", "Empleado guardado.")
            self.limpiar(); self.cargar_empleados()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error de Duplicado", "El Email o Teléfono ya existe.")
        finally: conn.close()

    def actualizar(self):
        if not self.id_empleado_seleccionado: return
        conn, cursor = db_conexion.conectar()
        try:
            rol_id = self.mapa_roles.get(self.cbo_rol.get())
            sql = "UPDATE Empleados SET nombre=?, apellido=?, telefono=?, email=?, rol_id=?, activo=? WHERE empleado_id=?"
            cursor.execute(sql, (self.entry_nombre.get(), self.entry_apellido.get(), self.entry_telefono.get(), self.entry_email.get(), rol_id, self.var_activo.get(), self.id_empleado_seleccionado))
            cursor.execute("DELETE FROM Empleado_Especialidad WHERE empleado_id=?", (self.id_empleado_seleccionado,))
            cursor.execute("DELETE FROM Horarios_Empleado WHERE empleado_id=?", (self.id_empleado_seleccionado,))
            self._guardar_detalles(cursor, self.id_empleado_seleccionado)
            conn.commit()
            messagebox.showinfo("OK", "Actualizado."); self.limpiar(); self.cargar_empleados()
        except Exception as e:
            conn.rollback(); messagebox.showerror("Error", str(e))
        finally: conn.close()

    def _guardar_detalles(self, cursor, eid):
        for esp_id, var in self.vars_especialidades.items():
            if var.get(): cursor.execute("INSERT INTO Empleado_Especialidad VALUES (?,?)", (eid, esp_id))
        for c in self.controles_horario:
            if c['chk'].get():
                cursor.execute("INSERT INTO Horarios_Empleado (empleado_id, dia_semana, hora_inicio, hora_fin) VALUES (?,?,?,?)",
                               (eid, c['dia'], c['ini'].get(), c['fin'].get()))

    def eliminar(self):
        if not self.id_empleado_seleccionado: return
        if messagebox.askyesno("Confirmar", "¿Eliminar empleado permanentemente?"):
            conn, cursor = db_conexion.conectar()
            try:
                
                cursor.execute("DELETE FROM Empleado_Especialidad WHERE empleado_id=?", (self.id_empleado_seleccionado,))
                cursor.execute("DELETE FROM Horarios_Empleado WHERE empleado_id=?", (self.id_empleado_seleccionado,))
                cursor.execute("DELETE FROM Empleados WHERE empleado_id=?", (self.id_empleado_seleccionado,))
                conn.commit()
                messagebox.showinfo("Éxito", "Empleado eliminado.")
            except Exception as e:
                conn.rollback()
                if "REFERENCE constraint" in str(e):
                    if messagebox.askyesno("Historial Detectado", "Este empleado tiene movimientos de inventario o ventas y NO puede borrarse.\n\n¿Deseas desactivarlo (dar de baja) en su lugar?"):
                        db_conexion.ejecutar_consulta("UPDATE Empleados SET activo = 0 WHERE empleado_id=?", (self.id_empleado_seleccionado,))
                        messagebox.showinfo("Baja Lógica", "El empleado ha sido marcado como INACTIVO.")
                else:
                    messagebox.showerror("Error", str(e))
            finally: 
                conn.close()
                self.limpiar(); self.cargar_empleados()

    def seleccionar(self, event):
        item = self.tree.focus()
        if not item: return
        vals = self.tree.item(item, 'values')
        self.id_empleado_seleccionado = vals[0]
        res = db_conexion.ejecutar_consulta("SELECT * FROM Empleados WHERE empleado_id=?", (self.id_empleado_seleccionado,), es_select=True)
        if res:
            d = res[0]
            self.entry_nombre.delete(0,"end"); self.entry_nombre.insert(0, d['nombre'])
            self.entry_apellido.delete(0,"end"); self.entry_apellido.insert(0, d['apellido'] or "")
            self.entry_telefono.delete(0,"end"); self.entry_telefono.insert(0, d['telefono'] or "")
            self.entry_email.delete(0,"end"); self.entry_email.insert(0, d['email'] or "")
            self.var_activo.set(1 if d['activo'] else 0)
            self.cbo_rol.set(vals[3])
            for v in self.vars_especialidades.values(): v.set(0)
            for c in self.controles_horario: c['chk'].set(0); c['ini'].delete(0,"end"); c['fin'].delete(0,"end")
            esps = db_conexion.ejecutar_consulta("SELECT especialidad_id FROM Empleado_Especialidad WHERE empleado_id=?", (self.id_empleado_seleccionado,), es_select=True)
            for e in (esps or []):
                if e['especialidad_id'] in self.vars_especialidades: self.vars_especialidades[e['especialidad_id']].set(1)
            hors = db_conexion.ejecutar_consulta("SELECT dia_semana, hora_inicio, hora_fin FROM Horarios_Empleado WHERE empleado_id=?", (self.id_empleado_seleccionado,), es_select=True)
            for h in (hors or []):
                idx = h['dia_semana'] - 1
                self.controles_horario[idx]['chk'].set(1)
                self.controles_horario[idx]['ini'].insert(0, str(h['hora_inicio'])[:5])
                self.controles_horario[idx]['fin'].insert(0, str(h['hora_fin'])[:5])

    def limpiar(self):
        self.id_empleado_seleccionado = None
        self.entry_nombre.delete(0,"end"); self.entry_apellido.delete(0,"end")
        self.entry_telefono.delete(0,"end"); self.entry_email.delete(0,"end")
        self.var_activo.set(1)
        for v in self.vars_especialidades.values(): v.set(0)
        for c in self.controles_horario: c['chk'].set(0); c['ini'].delete(0,"end"); c['fin'].delete(0,"end")