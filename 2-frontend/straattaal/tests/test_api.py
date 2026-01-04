import os
import sys

# Add backend folder to sys.path so that 'utils' and 'backend' imports work
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
import app as appmod

client = TestClient(appmod.app)


def fake_sample_n(n, model, tokenizer, max_length, temperature):
    return [f"w{i}" for i in range(n)]


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_generate_defaults(monkeypatch):
    monkeypatch.setattr(appmod, "sample_n", fake_sample_n)
    resp = client.get("/generate")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 10


def test_generate_custom(monkeypatch):
    monkeypatch.setattr(appmod, "sample_n", fake_sample_n)
    resp = client.get("/generate?num_words=3&temperature=0.7")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3


def test_starred_lifecycle(monkeypatch):
    monkeypatch.setattr(appmod, "sample_n", fake_sample_n)
    # ensure clean state
    appmod.starred_words.clear()

    resp = client.get("/starred")
    assert resp.status_code == 200
    assert resp.json() == []

    # add
    resp = client.post("/starred", json={"word": "hello"})
    assert resp.status_code == 200
    assert "hello" in resp.json()

    # duplicate add should not duplicate
    resp = client.post("/starred", json={"word": "hello"})
    assert resp.status_code == 200
    assert resp.json().count("hello") == 1

    # remove
    resp = client.post("/unstarred", json={"word": "hello"})
    assert resp.status_code == 200
    assert "hello" not in resp.json()
