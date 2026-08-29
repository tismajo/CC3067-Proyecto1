from llm_client import LLMClient

llm = LLMClient()

print("--- Pregunta 1: Información sobre Alan Turing ---")
resp1 = llm.send_message("¿Quién fue Alan Turing?")
print("Respuesta LLM:\n", resp1)

print("\n--- Pregunta 2: Referencia contextual (¿En qué fecha nació?) ---")
resp2 = llm.send_message("¿En qué fecha nació?")
print("Respuesta LLM:\n", resp2)