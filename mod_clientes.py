import customtkinter as ctk
from tkinter import ttk, messagebox
import db_conexion

class ClienteFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.id_cliente_seleccionado = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self, text="ADMINISTRACIÓN DE CLIENTES", font=("Arial", 20, "bold"))
        self.lbl_titulo.grid(row=0, column=0, pady=10)

        self.frame_central = ctk.CTkFrame(self)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        
        self.tab_view = ctk.CTkTabview(self.frame_central, width=600, height=450)
        self.tab_view.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tab_datos = self.tab_view.add("Datos Personales")
        self.tab_ficha = self.tab_view.add("Ficha Técnica")

        self.entry_nombre = ctk.CTkEntry(self.tab_datos, placeholder_text="Nombre")
        self.entry_nombre.pack(pady=5, fill="x", padx=20)
        
        self.entry_apellido = ctk.CTkEntry(self.tab_datos, placeholder_text="Apellido")
        self.entry_apellido.pack(pady=5, fill="x", padx=20)

        self.entry_telefono = ctk.CTkEntry(self.tab_datos, placeholder_text="Teléfono")
        self.entry_telefono.pack(pady=5, fill="x", padx=20)

        self.entry_email = ctk.CTkEntry(self.tab_datos, placeholder_text="Email")
        self.entry_email.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(self.tab_ficha, text="Alergias:", anchor="w").pack(fill="x", padx=20)
        self.txt_alergias = ctk.CTkTextbox(self.tab_ficha, height=50)
        self.txt_alergias.pack(pady=(0, 5), fill="x", padx=20)

        ctk.CTkLabel(self.tab_ficha, text="Contraindicaciones Médicas:", anchor="w").pack(fill="x", padx=20)
        self.txt_contra = ctk.CTkTextbox(self.tab_ficha, height=50)
        self.txt_contra.pack(pady=(0, 5), fill="x", padx=20)

        ctk.CTkLabel(self.tab_ficha, text="Historial / Notas Técnicas:", anchor="w").pack(fill="x", padx=20)
        self.txt_notas = ctk.CTkTextbox(self.tab_ficha, height=80)
        self.txt_notas.pack(pady=(0, 5), fill="x", padx=20)

        self.frame_botones = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botones.pack(side="right", fill="y", padx=10, pady=20)

        ctk.CTkButton(self.frame_botones, text="Guardar Nuevo", fg_color="green", command=self.agregar_cliente).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Actualizar", fg_color="#1f538d", command=self.actualizar_cliente).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Eliminar", fg_color="red", command=self.eliminar_cliente).pack(pady=5, fill="x")
        ctk.CTkButton(self.frame_botones, text="Limpiar", fg_color="gray", command=self.limpiar_formulario).pack(pady=5, fill="x")

        columns = ("ID", "Nombre", "Apellido", "Teléfono", "Email")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        sql = "SELECT cliente_id, nombre, apellido, telefono, email FROM Clientes"
        datos = db_conexion.ejecutar_consulta(sql, es_select=True)
        if datos:
            for d in datos:
                self.tree.insert("", "end", values=(d['cliente_id'], d['nombre'], d['apellido'], d['telefono'], d['email']))

    def agregar_cliente(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        if not nombre or not telefono:
            messagebox.showwarning("Faltan datos", "Nombre y Teléfono son requeridos.")
            return

        conn, cursor = db_conexion.conectar()
        try:

            sql_c = "INSERT INTO Clientes (nombre, apellido, telefono, email) OUTPUT INSERTED.cliente_id VALUES (?, ?, ?, ?)"
            cursor.execute(sql_c, (nombre, self.entry_apellido.get(), telefono, self.entry_email.get()))
            cid = cursor.fetchone()[0]


            sql_d = "INSERT INTO Detalles_Cliente (cliente_id, alergias, contraindicaciones, notas_tecnicas) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_d, (cid, self.txt_alergias.get("1.0", "end-1c"), self.txt_contra.get("1.0", "end-1c"), self.txt_notas.get("1.0", "end-1c")))
            
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
            self.limpiar_formulario(); self.cargar_datos()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
        finally: conn.close()

    def seleccionar_cliente(self, event):
        item = self.tree.focus()
        if not item: return
        vals = self.tree.item(item, 'values')
        self.id_cliente_seleccionado = vals[0]
        
        self.entry_nombre.delete(0,"end"); self.entry_nombre.insert(0, vals[1])
        self.entry_apellido.delete(0,"end"); self.entry_apellido.insert(0, vals[2] if vals[2]!='None' else '')
        self.entry_telefono.delete(0,"end"); self.entry_telefono.insert(0, vals[3])
        self.entry_email.delete(0,"end"); self.entry_email.insert(0, vals[4] if vals[4]!='None' else '')

        sql = "SELECT alergias, contraindicaciones, notas_tecnicas FROM Detalles_Cliente WHERE cliente_id=?"
        det = db_conexion.ejecutar_consulta(sql, (self.id_cliente_seleccionado,), es_select=True)
        
        self.txt_alergias.delete("1.0","end"); self.txt_contra.delete("1.0", "end"); self.txt_notas.delete("1.0","end")
        if det:
            self.txt_alergias.insert("1.0", det[0]['alergias'] or "")
            self.txt_contra.insert("1.0", det[0]['contraindicaciones'] or "")
            self.txt_notas.insert("1.0", det[0]['notas_tecnicas'] or "")

    def actualizar_cliente(self):
        if not self.id_cliente_seleccionado: return
        conn, cursor = db_conexion.conectar()
        try:
            cursor.execute("UPDATE Clientes SET nombre=?, apellido=?, telefono=?, email=? WHERE cliente_id=?",
                           (self.entry_nombre.get(), self.entry_apellido.get(), self.entry_telefono.get(), self.entry_email.get(), self.id_cliente_seleccionado))
            
            cursor.execute("UPDATE Detalles_Cliente SET alergias=?, contraindicaciones=?, notas_tecnicas=? WHERE cliente_id=?",
                           (self.txt_alergias.get("1.0","end-1c"), self.txt_contra.get("1.0", "end-1c"), self.txt_notas.get("1.0","end-1c"), self.id_cliente_seleccionado))
            conn.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado.")
            self.limpiar_formulario(); self.cargar_datos()
        except Exception as e:
            conn.rollback(); messagebox.showerror("Error", str(e))
        finally: conn.close()

    def eliminar_cliente(self):
        if not self.id_cliente_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un cliente de la lista.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente permanentemente?"):
            conn, cursor = db_conexion.conectar()
            try:
                # 1. Intentar borrar (Detalles_Cliente se borra solo por ON DELETE CASCADE en SQL)
                cursor.execute("DELETE FROM Clientes WHERE cliente_id=?", (self.id_cliente_seleccionado,))
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado.")
                self.limpiar_formulario(); self.cargar_datos()
            except Exception as e:
                conn.rollback()
                
                if "REFERENCE constraint" in str(e):
                    messagebox.showerror("Error de Integridad", 
                        "No se puede eliminar este cliente porque tiene HISTORIAL DE VENTAS.\n\n"
                        "Para mantener la contabilidad, el cliente debe permanecer en la base de datos.")
                else:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            finally: conn.close()

    def limpiar_formulario(self):
        self.id_cliente_seleccionado = None
        for entry in [self.entry_nombre, self.entry_apellido, self.entry_telefono, self.entry_email]: entry.delete(0,"end")
        for text in [self.txt_alergias, self.txt_contra, self.txt_notas]: text.delete("1.0","end")