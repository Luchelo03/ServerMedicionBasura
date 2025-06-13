import sqlite3

# Conexión a tu base de datos
conn = sqlite3.connect('mediciones.db')
cursor = conn.cursor()

# Borrar todos los registros de la tabla
cursor.execute("DELETE FROM mediciones")
conn.commit()

print("🧹 Todos los datos de la tabla 'mediciones' han sido eliminados.")

conn.close()
