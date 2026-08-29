from mcp.server.fastmcp import FastMCP
import tools

# Inicializar el servidor MCP
mcp = FastMCP("BibliotecaServer")


@mcp.tool()
def buscar_libros_tool(query: str = None, tema: str = None) -> str:
    """
    Permite consultar el catálogo de libros por palabra clave en el título o por tema (ej. 'Redes').
    Retorna la lista de libros encontrados y sus ejemplares disponibles.
    """
    libros = tools.buscar_libros(query=query, tema=tema)
    if not libros:
        return "No se encontraron libros que coincidan con la búsqueda."
    return str(libros)


@mcp.tool()
def obtener_cita_apa_tool(libro_id: int) -> str:
    """
    Genera la cita bibliográfica en formato APA 7 para un libro según su ID.
    """
    return tools.obtener_cita_apa(libro_id)


@mcp.tool()
def reservar_libro_tool(usuario_id: int, libro_id: int) -> str:
    """
    Reserva un ejemplar de un libro para un usuario específico dado su ID de usuario y el ID del libro.
    """
    resultado = tools.reservar_libro(usuario_id, libro_id)
    return str(resultado)


@mcp.tool()
def buscar_alternativas_tool(libro_id: int) -> str:
    """
    Encuentra libros alternativos del mismo tema que sí tienen ejemplares disponibles.
    """
    alternativas = tools.buscar_alternativas(libro_id)
    if not alternativas:
        return "No se encontraron libros alternativos disponibles para el tema."
    return str(alternativas)


if __name__ == "__main__":
    # Iniciar el servidor mediante comunicación STDIO
    mcp.run()