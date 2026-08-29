import asyncio

from mcp_host import MCPHost


async def main():
    host = MCPHost()

    try:
        await host.start_mcp_server()

        print(
            "--- Test 1: Buscar recomendación "
            "de libros de Redes ---"
        )

        respuesta1 = await host.send_user_message(
            "Dame recomendaciones de libros sobre redes"
        )

        print(
            "Respuesta final del asistente:\n",
            respuesta1,
        )

        print(
            "\n--- Test 2: Solicitar cita en APA 7 "
            "(manteniendo contexto) ---"
        )

        respuesta2 = await host.send_user_message(
            "Dame la cita en APA 7 de Redes de Computadoras: "
            "Un Enfoque Descendente"
        )

        print(
            "Respuesta final del asistente:\n",
            respuesta2,
        )

    finally:
        await host.close()


if __name__ == "__main__":
    asyncio.run(main())