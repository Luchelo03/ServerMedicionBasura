from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
from utils.sheets import obtener_altura_tacho
import os

app = Flask(__name__)

# TOKEN SECRETO COMPARTIDO
API_TOKEN = os.getenv("API_TOKEN")

@app.route('/medicion', methods=['POST'])
def recibir_medicion():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "No autorizado"}), 401

    data = request.json
    print("📥 Datos recibidos:", data)

    tacho_id = data.get('tacho_id')
    distancia = float(data['distancia'])

     # Validar que tacho_id sea del tipo 'TCH###'
    if not isinstance(tacho_id, str) or not tacho_id.startswith("TCH") or len(tacho_id) != 6:
        return jsonify({"error": "Formato inválido de tacho_id"}), 400

    # Validar que distancia sea un número positivo
    try:
        distancia = float(distancia)
        if distancia < 0:
            return jsonify({"error": "La distancia debe ser positiva"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "Distancia inválida"}), 400
    
    print("Validaciones pasadas ✅")

    altura_total = obtener_altura_tacho(tacho_id)
    print("altura: ", altura_total)
    
    if altura_total is None:
        return jsonify({'error': 'Tacho no encontrado'}), 404

    porcentaje = max(0, min(100, ((altura_total - distancia) / altura_total) * 100))
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('mediciones.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mediciones (tacho_id, distancia_libre_cm, porcentaje_lleno, fecha_hora)
        VALUES (?, ?, ?, ?)
    ''', (tacho_id, distancia, porcentaje, fecha_hora))
    conn.commit()
    conn.close()

    return jsonify({
        'status': 'OK',
        'porcentaje': porcentaje,
        'fecha_hora': fecha_hora,
    })

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
