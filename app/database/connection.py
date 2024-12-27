import sqlite3
import os

def get_db_connection():
    # Obtener la ruta absoluta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta a la base de datos
    db_path = os.path.join(current_dir, 'BancoLosko.db')
    
    # Crear la conexión
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    
    return connection