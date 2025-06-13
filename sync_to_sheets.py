import os
import json
from dotenv import load_dotenv
import tempfile
import sqlite3
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


# Convertir el contenido JSON del env a un diccionario
credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
# Crear archivo temporal
with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as temp:
    json.dump(credentials_info, temp)
    temp_path = temp.name

SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID_MEDICIONES")
RANGO = os.getenv("GOOGLE_RANGE_MEDICIONES")

# Autenticación con Google Sheets
credentials = service_account.Credentials.from_service_account_file(
    temp_path,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# === Función para obtener el último ID en Google Sheets ===
def obtener_ultimo_id():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A:A').execute()
    values = result.get('values', [])
    if not values or len(values) == 1:
        return 0
    ultimo = values[-1][0]  # e.g., 'M051'
    return int(ultimo[1:]) if ultimo.startswith('M') else 0

# Conexión a la base de datos
conn = sqlite3.connect('mediciones.db')
cursor = conn.cursor()

# Obtener filas no enviadas
cursor.execute("SELECT id, tacho_id, distancia_libre_cm, porcentaje_lleno, fecha_hora FROM mediciones WHERE enviado = 0")
rows = cursor.fetchall()

if rows:
    data = []
    ids = []

    next_id = obtener_ultimo_id() + 1

    for row in rows:
        id_, tacho_id, distancia, porcentaje, fecha = row
        nuevo_id = f"M{next_id:03}"  # Formato M001, M002, etc.
        data.append([nuevo_id, tacho_id, distancia, porcentaje, fecha])
        ids.append((id_,))
        next_id += 1

    # === Enviar a Google Sheets ===
    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGO,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': data}
    )
    response = request.execute()
    print("📤 Datos enviados a Google Sheets.")

    # === Marcar como enviados en SQLite ===
    cursor.executemany("UPDATE mediciones SET enviado = 1 WHERE id = ?", ids)
    conn.commit()
    print("✅ Registros actualizados en SQLite.")
else:
    print("🟡 No hay datos nuevos para enviar.")

conn.close()
