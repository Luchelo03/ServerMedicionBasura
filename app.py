from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
from utils.sheets import obtener_altura_tacho
import os

app = Flask(__name__)

@app.route('/medicion', methods=['POST'])
def recibir_medicion():
    data = request.json
    print("📥 Datos recibidos:", data)

    tacho_id = data.get('tacho_id')
    if data is None or 'distancia' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    distancia = float(data['distancia'])

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
        'fecha_hora': fecha_hora
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
