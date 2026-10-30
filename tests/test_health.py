from fastapi.testclient import TestClient

from llmwiki.main import app

client = TestClient(app)


def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"]


def test_health_reports_llm_not_configured_by_default():
    resp = client.get("/health")
    assert isinstance(resp.json()["llm_configured"], bool)
