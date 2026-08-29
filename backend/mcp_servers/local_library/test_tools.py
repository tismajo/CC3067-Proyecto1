import tools

print("--- 1. Probar Búsqueda por Tema 'Redes' ---")
print(tools.buscar_libros(tema="Redes"))

print("\n--- 2. Probar Cita APA 7 para libro ID 3 (Kurose & Ross) ---")
print(tools.obtener_cita_apa(3))

print("\n--- 3. Alternativas para el libro ID 4 (Stallings - sin stock) ---")
print(tools.buscar_alternativas(4))