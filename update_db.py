import sqlite3

conn = sqlite3.connect('mediciones.db')
cursor = conn.cursor()

# Añadir columna 'enviado' si no existe
cursor.execute("ALTER TABLE mediciones ADD COLUMN enviado INTEGER DEFAULT 0")
conn.commit()
conn.close()

print("✅ Columna 'enviado' añadida.")
