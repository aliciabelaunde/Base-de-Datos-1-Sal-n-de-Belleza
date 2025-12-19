import pyodbc
from tkinter import messagebox

CONN_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.;" 
    "Database=SalonDB;"
    "Trusted_Connection=yes;"
)

def get_connection():
    """Retorna la conexión cruda para transacciones manuales (Ventas)."""
    try:
        return pyodbc.connect(CONN_STRING)
    except pyodbc.Error as exc:
        print(f"Error get_connection: {exc}")
        return None

def conectar():
    """Retorna conn y cursor para consultas normales."""
    try:
        conn = pyodbc.connect(CONN_STRING)
        cursor = conn.cursor()
        return conn, cursor
    except pyodbc.Error as exc:
        messagebox.showerror("Error SQL", f"No se pudo conectar: {exc}")
        return None, None

def ejecutar_consulta(sql, parametros=None, es_select=False):
    conn, cursor = conectar()
    if conn is None: return [] if es_select else False
    
    try:
        if parametros: cursor.execute(sql, parametros)
        else: cursor.execute(sql)
        
        if es_select:
            cols = [col[0] for col in cursor.description]
            return [dict(zip(cols, row)) for row in cursor.fetchall()]
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return [] if es_select else False
    finally:
        conn.close()