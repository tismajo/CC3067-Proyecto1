from .db_connection import get_db_connection

def buscar_libros(query: str = None, tema: str = None):
    """
    Busca libros en el catálogo por título/descripción o por nombre del tema.
    Retorna los datos del libro junto con la cantidad de ejemplares disponibles.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT 
                    l.id,
                    l.titulo,
                    l.subtitulo,
                    l.anio_publicacion,
                    e.nombre AS editorial,
                    GROUP_CONCAT(DISTINCT CONCAT(a.nombres, ' ', a.apellidos) ORDER BY la.orden_autoria SEPARATOR ', ') AS autores,
                    GROUP_CONCAT(DISTINCT t.nombre SEPARATOR ', ') AS temas,
                    COUNT(DISTINCT CASE WHEN ej.estado = 'DISPONIBLE' THEN ej.id END) AS ejemplares_disponibles
                FROM libro l
                LEFT JOIN editorial e ON l.editorial_id = e.id
                LEFT JOIN libro_autor la ON l.id = la.libro_id
                LEFT JOIN autor a ON la.autor_id = a.id
                LEFT JOIN libro_tema lt ON l.id = lt.libro_id
                LEFT JOIN tema t ON lt.tema_id = t.id
                LEFT JOIN ejemplar ej ON l.id = ej.libro_id
                WHERE 1=1
            """
            params = []
            if query:
                sql += " AND (l.titulo LIKE %s OR l.descripcion LIKE %s)"
                params.extend([f"%{query}%", f"%{query}%"])
            if tema:
                sql += " AND t.nombre LIKE %s"
                params.append(f"%{tema}%")

            sql += " GROUP BY l.id;"
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        connection.close()


def obtener_cita_apa(libro_id: int) -> str:
    """
    Genera y retorna la referencia bibliográfica formateada en APA 7 para un libro.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Obtener datos del libro y editorial
            sql_libro = """
                SELECT l.titulo, l.anio_publicacion, l.numero_edicion, e.nombre AS editorial
                FROM libro l
                LEFT JOIN editorial e ON l.editorial_id = e.id
                WHERE l.id = %s;
            """
            cursor.execute(sql_libro, (libro_id,))
            libro = cursor.fetchone()

            if not libro:
                return f"Error: No se encontró el libro con ID {libro_id}."

            # Obtener autores ordenados por orden_autoria
            sql_autores = """
                SELECT a.nombres, a.apellidos
                FROM autor a
                JOIN libro_autor la ON a.id = la.autor_id
                WHERE la.libro_id = %s
                ORDER BY la.orden_autoria ASC;
            """
            cursor.execute(sql_autores, (libro_id,))
            autores = cursor.fetchall()

            if not autores:
                autores_str = "Autor desconocido"
            else:
                formatted_autores = []
                for a in autores:
                    primer_nombre_inicial = a["nombres"][0] + "." if a["nombres"] else ""
                    formatted_autores.append(f"{a['apellidos']}, {primer_nombre_inicial}")
                
                if len(formatted_autores) == 1:
                    autores_str = formatted_autores[0]
                elif len(formatted_autores) == 2:
                    autores_str = f"{formatted_autores[0]} & {formatted_autores[1]}"
                else:
                    autores_str = ", ".join(formatted_autores[:-1]) + f", & {formatted_autores[-1]}"

            edicion_str = f" ({libro['numero_edicion']}a ed.)" if libro["numero_edicion"] and libro["numero_edicion"] > 1 else ""
            editorial_str = f". {libro['editorial']}" if libro["editorial"] else ""

            return f"{autores_str} ({libro['anio_publicacion']}). {libro['titulo']}{edicion_str}{editorial_str}."
    finally:
        connection.close()


def reservar_libro(usuario_id: int, libro_id: int) -> dict:
    """
    Crea una reserva para un libro. Si hay un ejemplar disponible, asigna el ejemplar
    y cambia su estado a 'RESERVADO'.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Verificar si hay ejemplares disponibles
            sql_ejemplar = """
                SELECT id FROM ejemplar 
                WHERE libro_id = %s AND estado = 'DISPONIBLE' 
                LIMIT 1;
            """
            cursor.execute(sql_ejemplar, (libro_id,))
            ejemplar = cursor.fetchone()

            ejemplar_id = ejemplar["id"] if ejemplar else None
            
            # Registrar la reserva
            sql_reserva = """
                INSERT INTO reserva (usuario_id, libro_id, ejemplar_id, estado)
                VALUES (%s, %s, %s, 'PENDIENTE');
            """
            cursor.execute(sql_reserva, (usuario_id, libro_id, ejemplar_id))
            reserva_id = cursor.lastrowid

            # Si se asignó un ejemplar, actualizar su estado
            if ejemplar_id:
                sql_update = "UPDATE ejemplar SET estado = 'RESERVADO' WHERE id = %s;"
                cursor.execute(sql_update, (ejemplar_id,))

            return {
                "reserva_id": reserva_id,
                "libro_id": libro_id,
                "ejemplar_id": ejemplar_id,
                "estado": "CONFIRMADA" if ejemplar_id else "PENDIENTE (Sin ejemplar disponible inmediato)"
            }
    finally:
        connection.close()


def buscar_alternativas(libro_id: int) -> list:
    """
    Busca libros alternativos del mismo tema o autor que tengan ejemplares disponibles.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT DISTINCT
                    l.id,
                    l.titulo,
                    l.anio_publicacion,
                    COUNT(DISTINCT ej.id) AS ejemplares_disponibles
                FROM libro l
                JOIN libro_tema lt ON l.id = lt.libro_id
                JOIN ejemplar ej ON l.id = ej.libro_id
                WHERE lt.tema_id IN (SELECT tema_id FROM libro_tema WHERE libro_id = %s)
                  AND l.id != %s
                  AND ej.estado = 'DISPONIBLE'
                GROUP BY l.id;
            """
            cursor.execute(sql, (libro_id, libro_id))
            return cursor.fetchall()
    finally:
        connection.close()