import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import tempfile

load_dotenv()



def obtener_altura_tacho(tacho_id):
    # Convertir el contenido JSON del env a un diccionario
    credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as temp:
        json.dump(credentials_info, temp)
        temp_path = temp.name

    creds = service_account.Credentials.from_service_account_file(
        temp_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )

    sheet_id = os.getenv("GOOGLE_SHEETS_ID_TACHOS")
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=sheet_id, range="Hoja 1!A2:H").execute()
    values = result.get('values', [])

    for row in values:
        if len(row) >= 8 and row[2] == tacho_id:
            return float(row[7])  # columna AlturaCM
    return None
