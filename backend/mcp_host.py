import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()

BACKEND_DIR = Path(__file__).resolve().parent
LOGS_DIR = BACKEND_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / "mcp_interactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MCPHost:

    def __init__(self, model: str = "gemini-3.6-flash"):
        api_key = os.getenv("AGENT_API_KEY")

        if not api_key:
            raise ValueError(
                "No se encontró AGENT_API_KEY en las variables de entorno."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model

        self.session = None
        self.chat = None
        self.tools_map = {}

        self._stdio_context = None
        self._session_context = None

        self.system_prompt = (
            "Eres el asistente oficial de la biblioteca UVG. "
            "Para responder sobre libros, disponibilidad, citas APA 7 "
            "y reservas, DEBES invocar las herramientas MCP disponibles. "
            "No inventes información del catálogo."
        )

    async def start_mcp_server(self):
        """Conecta con el servidor MCP local mediante STDIO."""

        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_servers.local_library.server"],
            cwd=str(BACKEND_DIR),
            env=os.environ.copy(),
        )

        self._stdio_context = stdio_client(server_params)

        read_stream, write_stream = (
            await self._stdio_context.__aenter__()
        )

        self._session_context = ClientSession(
            read_stream,
            write_stream,
        )

        self.session = await self._session_context.__aenter__()
        await self.session.initialize()

        tools_response = await self.session.list_tools()
        mcp_tools = tools_response.tools

        gemini_tools = []

        for tool in mcp_tools:
            self.tools_map[tool.name] = tool

            schema = getattr(
                tool,
                "inputSchema",
                {
                    "type": "object",
                    "properties": {},
                },
            )

            function_declaration = types.FunctionDeclaration(
                name=tool.name,
                description=tool.description or "",
                parameters=schema,
            )

            gemini_tools.append(
                types.Tool(
                    function_declarations=[function_declaration]
                )
            )

        self.chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                tools=gemini_tools,
                temperature=0.2,
            ),
        )

        print(
            "Servidor MCP conectado y herramientas cargadas "
            "exitosamente."
        )

        print("Herramientas disponibles:")

        for tool_name in self.tools_map:
            print(f"  - {tool_name}")

    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> str:
        """Ejecuta una herramienta MCP y registra la interacción."""

        if self.session is None:
            raise RuntimeError(
                "No existe una sesión MCP activa."
            )

        log_payload = {
            "type": "REQUEST_MCP",
            "tool": tool_name,
            "params": arguments,
        }

        logging.info(
            json.dumps(log_payload, ensure_ascii=False)
        )

        result = await self.session.call_tool(
            tool_name,
            arguments,
        )

        response_text = (
            result.content[0].text
            if result.content
            else str(result)
        )

        log_response = {
            "type": "RESPONSE_MCP",
            "tool": tool_name,
            "result": response_text,
        }

        logging.info(
            json.dumps(log_response, ensure_ascii=False)
        )

        return response_text

    async def send_user_message(self, user_text: str) -> str:
        """Envía un mensaje al LLM y procesa llamadas MCP."""

        if self.chat is None:
            raise RuntimeError(
                "El host no ha sido inicializado. "
                "Ejecuta start_mcp_server() primero."
            )

        response = self.chat.send_message(
            message=user_text
        )

        function_calls = response.function_calls or []

        for call in function_calls:
            tool_name = call.name
            arguments = dict(call.args or {})

            print(
                "\n[MCP HOST] El LLM solicitó ejecutar: "
                f"{tool_name}({arguments})"
            )

            tool_result = await self.execute_tool(
                tool_name,
                arguments,
            )

            print(
                "[MCP HOST] Resultado del servidor MCP: "
                f"{tool_result}\n"
            )

            function_response = (
                types.Part.from_function_response(
                    name=tool_name,
                    response={
                        "result": tool_result,
                    },
                )
            )

            response = self.chat.send_message(
                message=function_response
            )

        return response.text

    async def close(self):
        """Cierra la sesión y el subproceso MCP."""

        if self._session_context is not None:
            await self._session_context.__aexit__(
                None,
                None,
                None,
            )
            self._session_context = None
            self.session = None

        if self._stdio_context is not None:
            await self._stdio_context.__aexit__(
                None,
                None,
                None,
            )
            self._stdio_context = None