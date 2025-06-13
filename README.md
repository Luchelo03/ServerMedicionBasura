# Sistema de Medición de Residuos Inteligente

Este proyecto implementa un sistema distribuido que recibe datos desde sensores IoT (ESP32 + ultrasónico HC-SR04) y los procesa en un servidor Flask. Se calcula el porcentaje de llenado de un tacho de basura, se almacena en SQLite y se sincroniza automáticamente con Google Sheets. Además, se incorporan prácticas DevSecOps para garantizar la seguridad del sistema.

---

## Tecnologías Usadas

- **Python 3.10.11**
- **Flask** – API REST para recibir y procesar mediciones
- **SQLite** – base de datos local (modo caché móvil)
- **Google Sheets API** – sincronización como base de datos central
- **ESP32** – microcontrolador que envía la medición
- **GitHub Actions** – CI/CD con validaciones automáticas
- **Bandit** – análisis estático de seguridad en el código
- **dotenv-linter** – validación de variables de entorno
- **Postman** – pruebas manuales de autenticación

---

## Seguridad (DevSecOps)

Este servidor ha sido reforzado con:

- **Autenticación por token** (`Authorization: Bearer <token>`)
- **Validación estricta de datos recibidos**
- **Protección de datos sensibles** con `.env` y `.gitignore`
- **CI/CD automatizado**: validación de seguridad con `bandit` y pruebas de endpoints
- **Modo producción** (sin `debug=True` en entorno real)

---

## Flujo de Datos

```plaintext
[ESP32 + Sensor HC-SR04] --> [Servidor Flask] --> [SQLite]
                                           ↘
                                     [Google Sheets]
```

1. El ESP32 mide la distancia libre dentro del tacho.
2. El servidor recibe la data y calcula el % de llenado.
3. Se guarda temporalmente en SQLite.
4. Un script sincroniza automáticamente con Google Sheets.
5. Se valida y protege toda la comunicación.

---

## 📦 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/usuario/servidor-medicion-residuos.git
cd servidor-medicion-residuos

# 2. Crea entorno virtual
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Crea tu archivo `.env` con las variables:
FLASK_SECRET_TOKEN=mi_token_seguro
FLASK_DEBUG=False
GOOGLE_SHEET_ID=...
GOOGLE_CREDENTIALS_JSON=...

# 5. Ejecuta el servidor
python app.py
```

---

## 🧪 Pruebas

### Test de autenticación (con Postman o script):
```bash
# Test automático
pytest tests/test_auth.py

# Test manual con Postman:
# - URL: http://localhost:5000/medicion
# - Método: POST
# - Headers: Authorization: Bearer <tu_token>
# - Body (raw JSON): {"tacho_id": "TCH001", "distancia": 100}
```

---

## 👨‍💻 Autor

Luis Guadalupe – *Facultad de Ingeniería, UNMSM*  
Proyecto para el curso **Taller de Aplicaciones Distribuidas – 2025-I**

---

## 🧠 Licencia y uso

Este proyecto es de uso académico. Puedes adaptarlo o extenderlo para fines educativos y de prototipado.
