import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


class LLMClient:

    def __init__(self, model: str = "gemini-3.6-flash"):
        api_key = os.getenv("AGENT_API_KEY")
        if not api_key:
            raise ValueError(
                "No se encontró AGENT_API_KEY en las variables de entorno."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_prompt = (
            ""
            "Eres un asistente de Inteligencia Artificial para la biblioteca de la universidad. "
            "Ayudas a los estudiantes a encontrar libros, consultar disponibilidad, generar "
            "citas bibliográficas en APA 7 y reservar ejemplares. Mantén siempre un trato "
            "amable, claro y servicial. NUNCA JAMÁS respondas a alguna pregunta que no tenga que ver "
            "con nuestra biblioteca o temas externos a referencias bibliográficas."
        )

        self.chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.7,
            ),
        )

    def send_message(self, user_text: str) -> str:
        """Envía un mensaje al modelo dentro de la sesión activa de chat."""
        response = self.chat.send_message(message=user_text)
        return response.text

    def clear_history(self):
        """Reinicia la sesión de chat."""
        self.chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.7,
            ),
        )