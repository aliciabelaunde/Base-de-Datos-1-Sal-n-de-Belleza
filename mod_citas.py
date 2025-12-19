import customtkinter as ctk
from tkinter import ttk, messagebox, simpledialog
import db_conexion
from datetime import datetime, timedelta

class CitaFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.id_cita = None
        self.map_clientes = {}  
        self.map_empleados = {} 
        self.map_estados = {} 
        self.vars_servicios = {} 
        self.info_servicios = {} 

        
        ctk.CTkLabel(self, text="GESTIÓN DE CITAS", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=10)

        
        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        
        
        self.frame_form = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_form.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        
        ctk.CTkLabel(self.frame_form, text="Cliente:").pack(anchor="w")
        self.combo_clientes = ctk.CTkComboBox(self.frame_form, width=250)
        self.combo_clientes.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.frame_form, text="Atendido por:").pack(anchor="w")
        self.combo_empleados = ctk.CTkComboBox(self.frame_form, width=250)
        self.combo_empleados.pack(fill="x", pady=(0, 10))

        frame_tiempo = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        frame_tiempo.pack(fill="x", pady=5)
        
        self.entry_fecha = ctk.CTkEntry(frame_tiempo, placeholder_text="YYYY-MM-DD")
        self.entry_fecha.pack(side="left", fill="x", expand=True, padx=(0,5))
        
        self.entry_hora = ctk.CTkEntry(frame_tiempo, placeholder_text="HH:MM (24h)")
        self.entry_hora.pack(side="right", fill="x", expand=True, padx=(5,0))
        
        ctk.CTkButton(self.frame_form, text="Usar Fecha/Hora Actual", height=20, 
                      command=self.poner_hora_actual, fg_color="gray").pack(anchor="e", pady=(0,10))

        ctk.CTkLabel(self.frame_form, text="Estado Actual:").pack(anchor="w")
        self.combo_estados = ctk.CTkComboBox(self.frame_form, width=250)
        self.combo_estados.pack(fill="x", pady=(0, 10))

        self.frame_servs = ctk.CTkFrame(self.frame_central)
        self.frame_servs.pack(side="right", fill="both", padx=10, pady=10, ipadx=5)
        
        ctk.CTkLabel(self.frame_servs, text="Servicios a Realizar:", font=("Arial", 12, "bold")).pack(pady=5)
        self.scroll_servs = ctk.CTkScrollableFrame(self.frame_servs, width=250, height=200)
        self.scroll_servs.pack(fill="both", expand=True, padx=5, pady=5)

        self.frame_botones = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botones.pack(side="bottom", fill="x", padx=10, pady=10)

        ctk.CTkButton(self.frame_botones, text="Agendar Cita", fg_color="green", command=self.guardar).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(self.frame_botones, text="Cancelar Cita", fg_color="#d32f2f", command=self.cancelar_cita).pack(side="left", expand=True, padx=5)

        cols = ("ID", "Fecha", "Hora", "Cliente", "Empleado", "Estado")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        
        self.tree.column("ID", width=40)
        self.tree.column("Fecha", width=90)
        self.tree.column("Hora", width=60)
        self.tree.column("Cliente", width=150)
        self.tree.column("Empleado", width=150)
        self.tree.column("Estado", width=100)

        for c in cols: self.tree.heading(c, text=c)
        
        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        self.cargar_datos_combos()
        self.cargar_tabla()

    def poner_hora_actual(self):
        now = datetime.now()
        self.entry_fecha.delete(0, "end"); self.entry_fecha.insert(0, now.strftime("%Y-%m-%d"))
        self.entry_hora.delete(0, "end"); self.entry_hora.insert(0, now.strftime("%H:%M"))

    def cargar_datos_combos(self):
        # 1. Clientes
        self.map_clientes = {}
        clientes = db_conexion.ejecutar_consulta("SELECT cliente_id, nombre, apellido FROM Clientes", es_select=True)
        vals_c = []
        if clientes:
            for c in clientes:
                nombre_full = f"{c['nombre']} {c['apellido']}"
                self.map_clientes[nombre_full] = c['cliente_id']
                vals_c.append(nombre_full)
        self.combo_clientes.configure(values=vals_c)

        self.map_empleados = {}
        emps = db_conexion.ejecutar_consulta("SELECT empleado_id, nombre, apellido FROM Empleados", es_select=True)
        vals_e = []
        if emps:
            for e in emps:
                nombre_full = f"{e['nombre']} {e['apellido']}"
                self.map_empleados[nombre_full] = e['empleado_id']
                vals_e.append(nombre_full)
        self.combo_empleados.configure(values=vals_e)

        self.map_estados = {}
        est = db_conexion.ejecutar_consulta("SELECT estado_id, nombre_estado FROM Estado_Cita", es_select=True)
        vals_s = []
        if est:
            for s in est:
                self.map_estados[s['nombre_estado']] = s['estado_id']
                vals_s.append(s['nombre_estado'])
        self.combo_estados.configure(values=vals_s)
        self.combo_estados.set("Pendiente") 

        for w in self.scroll_servs.winfo_children(): w.destroy()
        self.vars_servicios = {}
        self.info_servicios = {}
        servs = db_conexion.ejecutar_consulta("SELECT servicio_id, nombre_servicio, precio, duracion_minutos FROM Servicios", es_select=True)
        if servs:
            for s in servs:
                var = ctk.IntVar()
                sid = s['servicio_id']
                self.vars_servicios[sid] = var
                self.info_servicios[sid] = {'p': s['precio'], 'd': s['duracion_minutos']}
                
                txt = f"{s['nombre_servicio']} (${s['precio']:.0f})"
                ctk.CTkCheckBox(self.scroll_servs, text=txt, variable=var).pack(anchor="w", pady=2)

    def cargar_tabla(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        
        sql = """
        SELECT 
            c.cita_id, 
            c.fecha_hora_inicio, 
            cl.nombre AS cli_nombre, 
            cl.apellido AS cli_apellido, 
            em.nombre AS emp_nombre, 
            em.apellido AS emp_apellido, 
            es.nombre_estado
        FROM Citas c
        JOIN Clientes cl ON c.cliente_id = cl.cliente_id
        JOIN Empleados em ON c.empleado_id = em.empleado_id
        JOIN Estado_Cita es ON c.estado_id = es.estado_id
        ORDER BY c.fecha_hora_inicio DESC
        """
        datos = db_conexion.ejecutar_consulta(sql, es_select=True)
        if datos:
            for d in datos:
                dt = d['fecha_hora_inicio'] # Es objeto datetime de pyodbc
                fecha_str = dt.strftime("%Y-%m-%d")
                hora_str = dt.strftime("%H:%M")
                
                cli = f"{d['cli_nombre']} {d['cli_apellido']}"
                emp = f"{d['emp_nombre']} {d['emp_apellido']}"
                
                self.tree.insert("", "end", values=(d['cita_id'], fecha_str, hora_str, cli, emp, d['nombre_estado']))

    def guardar(self):

        cliente_txt = self.combo_clientes.get()
        emp_txt = self.combo_empleados.get()
        estado_txt = self.combo_estados.get()
        fecha_txt = self.entry_fecha.get()
        hora_txt = self.entry_hora.get()

        if not cliente_txt or not emp_txt or not fecha_txt or not hora_txt:
            messagebox.showwarning("Faltan datos", "Seleccione Cliente, Empleado, Fecha y Hora")
            return

        cid = self.map_clientes.get(cliente_txt)
        eid = self.map_empleados.get(emp_txt)
        stid = self.map_estados.get(estado_txt)

        try:
            str_inicio = f"{fecha_txt} {hora_txt}"
            dt_inicio = datetime.strptime(str_inicio, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error Fechas", "Formato incorrecto. Use YYYY-MM-DD y HH:MM")
            return

        
        servicios_seleccionados = []
        duracion_total = 0

        for sid, var in self.vars_servicios.items():
            if var.get() == 1:
                servicios_seleccionados.append(sid)
                duracion_total += self.info_servicios[sid]['d']

        if not servicios_seleccionados:
            messagebox.showwarning("Servicios", "Seleccione al menos un servicio")
            return

        dt_fin = dt_inicio + timedelta(minutes=duracion_total)

        conn, cursor = db_conexion.conectar()
        try:
            sql_cita = """
                INSERT INTO Citas (cliente_id, empleado_id, fecha_hora_inicio, fecha_hora_fin, estado_id)
                OUTPUT INSERTED.cita_id
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql_cita, (cid, eid, dt_inicio, dt_fin, stid))
            
            row = cursor.fetchone()
            if not row:
                raise Exception("Error crítico: No se obtuvo el ID de la cita nueva.")
            
            cita_id = int(row[0])

            sql_det = "INSERT INTO Detalle_Cita (cita_id, servicio_id, precio_cobrado, duracion_real_minutos) VALUES (?,?,?,?)"
            for sid in servicios_seleccionados:
                precio = self.info_servicios[sid]['p']
                duracion = self.info_servicios[sid]['d']
                cursor.execute(sql_det, (cita_id, sid, precio, duracion))

            conn.commit()
            messagebox.showinfo("Cita Agendada", f"Cita guardada.\nTermina aprox: {dt_fin.strftime('%H:%M')}")
            self.limpiar()
            self.cargar_tabla()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error SQL", f"Detalle del error: {str(e)}")
        finally:
            conn.close()

    def cancelar_cita(self):
        if not self.id_cita:
            messagebox.showwarning("Selección", "Seleccione una cita de la tabla para cancelar")
            return

        motivo = simpledialog.askstring("Cancelar Cita", "Motivo de la cancelación:")
        if not motivo: return 

        conn, cursor = db_conexion.conectar()
        try:
            cursor.execute("SELECT estado_id FROM Estado_Cita WHERE nombre_estado = 'Cancelada'")
            res = cursor.fetchone()
            if res is None or res[0] is None:
                raise Exception("Estado 'Cancelada' no existe en BD")

            id_cancelada = int(res[0])
            cursor.execute("UPDATE Citas SET estado_id = ? WHERE cita_id = ?", (id_cancelada, int(self.id_cita)))

            sql_can = "INSERT INTO Cancelaciones (cita_id, motivo, cancelado_por) VALUES (?, ?, ?)"
            cursor.execute(sql_can, (int(self.id_cita), motivo, 'Usuario Sistema'))

            conn.commit()
            messagebox.showinfo("Cancelada", "La cita ha sido cancelada oficialmente.")
            self.limpiar()
            self.cargar_tabla()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def seleccionar(self, event):
        item = self.tree.focus()
        if not item: return
        vals = self.tree.item(item, 'values')
        if vals:
            self.id_cita = vals[0]

    def limpiar(self):
        self.id_cita = None
        self.entry_fecha.delete(0, "end")
        self.entry_hora.delete(0, "end")
        self.combo_clientes.set("")
        self.combo_empleados.set("")
        self.combo_estados.set("Pendiente")
        for v in self.vars_servicios.values(): v.set(0)