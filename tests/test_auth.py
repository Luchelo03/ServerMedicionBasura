import requests

def test_authentication():
    r = requests.post("http://192.168.1.40:5000/medicion", json={"tacho_id": "TCH001", "distancia": 200})
    assert r.status_code == 401  # Esperamos que falle si no hay token
