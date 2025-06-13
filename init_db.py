import sqlite3

# Conectar o crear la base de datos local
conn = sqlite3.connect('mediciones.db')
cursor = conn.cursor()

# Crear la tabla de mediciones
cursor.execute('''
CREATE TABLE IF NOT EXISTS mediciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tacho_id TEXT NOT NULL,
    distancia_libre_cm REAL NOT NULL,
    porcentaje_lleno REAL NOT NULL,
    fecha_hora TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ Base de datos y tabla 'mediciones' creadas con éxito.")
