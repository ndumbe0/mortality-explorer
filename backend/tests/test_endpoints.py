from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get('/health')
    assert res.status_code == 200

def test_countries():
    res = client.get('/api/mortality/countries')
    assert res.status_code == 200
