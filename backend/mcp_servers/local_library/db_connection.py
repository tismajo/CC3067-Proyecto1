import os
import pymysql
from pymysql.cursors import DictCursor

# Configuración de conexión usando las credenciales del sistema
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "libraryu")
DB_PASSWORD = os.getenv("DB_PASSWORD", "B1b!10")
DB_NAME = os.getenv("DB_NAME", "librarydb")
DB_PORT = int(os.getenv("DB_PORT", 3306))


def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL.
    Retorna los resultados como diccionarios (DictCursor).
    """
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=DictCursor,
        autocommit=True
    )


def test_connection():
    """Prueba rápida de conectividad."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM biblioteca LIMIT 1;")
            result = cursor.fetchone()
            print("Conexión exitosa a MySQL.")
            print(f"Biblioteca encontrada: {result['nombre']}")
        connection.close()
        return True
    except Exception as e:
        print(f"Error al conectar a MySQL: {e}")
        return False


if __name__ == "__main__":
    test_connection()