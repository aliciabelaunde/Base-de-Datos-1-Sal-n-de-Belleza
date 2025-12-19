import customtkinter as ctk
from tkinter import messagebox
import db_conexion

from mod_clientes import ClienteFrame
from mod_empleados import EmpleadoFrame
from mod_servicios import ServicioFrame
from mod_promociones import PromocionFrame
from mod_citas import CitaFrame
from mod_productos import ProductoFrame
from mod_ventas import VentasFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión - Salón de Belleza")
        self.geometry("1100x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="ns")

        self.lbl_logo = ctk.CTkLabel(self.menu_frame, text="SALON MANAGER", font=("Arial", 20, "bold"))
        self.lbl_logo.pack(pady=30)

        self.btn_inicio = ctk.CTkButton(self.menu_frame, text="Inicio", command=self.ver_inicio, fg_color="transparent", border_width=1)
        self.btn_inicio.pack(pady=10, padx=20, fill="x")

        self.btn_clientes = ctk.CTkButton(self.menu_frame, text="Clientes", command=self.ver_clientes, fg_color="transparent", border_width=1)
        self.btn_clientes.pack(pady=10, padx=20, fill="x")
        
        self.btn_empleados = ctk.CTkButton(self.menu_frame, text="Empleados", command=self.ver_empleados, fg_color="transparent", border_width=1)
        self.btn_empleados.pack(pady=10, padx=20, fill="x")

        self.btn_servicios = ctk.CTkButton(self.menu_frame, text="Servicios", command=self.ver_servicios, fg_color="transparent", border_width=1)
        self.btn_servicios.pack(pady=10, padx=20, fill="x")

        self.btn_promos = ctk.CTkButton(self.menu_frame, text="Promociones", command=self.ver_promos, fg_color="transparent", border_width=1)
        self.btn_promos.pack(pady=10, padx=20, fill="x")

        self.btn_citas = ctk.CTkButton(self.menu_frame, text="Agenda / Citas", command=self.ver_citas, fg_color="transparent", border_width=1)
        self.btn_citas.pack(pady=10, padx=20, fill="x")

        self.btn_inv = ctk.CTkButton(self.menu_frame, text="Inventario", command=self.ver_inv, fg_color="transparent", border_width=1)
        self.btn_inv.pack(pady=10, padx=20, fill="x")

        self.btn_ventas = ctk.CTkButton(self.menu_frame, text="Caja / Ventas", command=self.ver_ventas, fg_color="transparent", border_width=1)
        self.btn_ventas.pack(pady=10, padx=20, fill="x")

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.view_inicio = ctk.CTkFrame(self.main_frame)
        ctk.CTkLabel(self.view_inicio, text="Bienvenido al Sistema", font=("Arial", 30)).pack(expand=True)

        ctk.CTkLabel(
            self.view_inicio, 
            text="by Alicia Belaunde", 
            font=("Arial", 15, "italic"), 
            text_color="gray"            
        ).pack(side="bottom", pady=10)

        self.view_clientes = ClienteFrame(self.main_frame)
        self.view_empleados = EmpleadoFrame(self.main_frame)
        self.view_servicios = ServicioFrame(self.main_frame)
        self.view_promos = PromocionFrame(self.main_frame) 
        self.view_citas = CitaFrame(self.main_frame)
        self.view_inv = ProductoFrame(self.main_frame)
        self.view_ventas = VentasFrame(self.main_frame)

        
        self.ver_inicio()

    def ocultar_todo(self):
        self.view_inicio.pack_forget()
        self.view_clientes.pack_forget()
        self.view_empleados.pack_forget()
        self.view_servicios.pack_forget()
        self.view_promos.pack_forget()
        self.view_citas.pack_forget()
        self.view_inv.pack_forget()
        self.view_ventas.pack_forget()
        
        self.btn_inicio.configure(fg_color="transparent")
        self.btn_clientes.configure(fg_color="transparent")
        self.btn_empleados.configure(fg_color="transparent")
        self.btn_servicios.configure(fg_color="transparent")
        self.btn_promos.configure(fg_color="transparent")
        self.btn_citas.configure(fg_color="transparent")
        self.btn_inv.configure(fg_color="transparent")
        self.btn_ventas.configure(fg_color="transparent")

    def ver_inicio(self):
        self.ocultar_todo()
        self.view_inicio.pack(fill="both", expand=True)
        self.btn_inicio.configure(fg_color=("gray75", "gray25"))

    def ver_clientes(self):
        self.ocultar_todo()
        self.view_clientes.pack(fill="both", expand=True)
        self.btn_clientes.configure(fg_color=("gray75", "gray25"))

    def ver_empleados(self):
        self.ocultar_todo()

        if hasattr(self.view_empleados, 'cargar_empleados'):
            self.view_empleados.cargar_empleados() 
            
        self.view_empleados.pack(fill="both", expand=True)
        self.btn_empleados.configure(fg_color=("gray75", "gray25"))

    def ver_servicios(self):
        self.ocultar_todo()
        self.view_servicios.pack(fill="both", expand=True)
        self.btn_servicios.configure(fg_color=("gray75", "gray25"))
    
    def ver_promos(self):
        self.ocultar_todo()
        self.view_promos.cargar_servicios_ui() 
        self.view_promos.pack(fill="both", expand=True)
        self.btn_promos.configure(fg_color=("gray75", "gray25"))
    
    def ver_citas(self):
        self.ocultar_todo()
        self.view_citas.cargar_datos_combos() 
        self.view_citas.cargar_tabla()        
        self.view_citas.pack(fill="both", expand=True)
        self.btn_citas.configure(fg_color=("gray75", "gray25"))
    
    def ver_inv(self):
        self.ocultar_todo()
        self.view_inv.cargar_combos() 
        self.view_inv.cargar_tablas_todas()
        self.view_inv.pack(fill="both", expand=True)
        self.btn_inv.configure(fg_color=("gray75", "gray25"))
    
    def ver_ventas(self):
        self.ocultar_todo()
        self.view_ventas.cargar_datos_iniciales() 
        self.view_ventas.pack(fill="both", expand=True)
        self.btn_ventas.configure(fg_color=("gray75", "gray25"))

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()