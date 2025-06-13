import requests

def test_authentication():
    r = requests.post("http://192.168.1.40:5000/medicion", json={"tacho_id": "TCH001", "distancia": 200}, timeout=5)
    if r.status_code != 401:
        raise Exception("Fallo de seguridad: el endpoint permite acceso sin token")

