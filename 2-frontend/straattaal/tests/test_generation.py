import os
import sys

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
import app as appmod

client = TestClient(appmod.app)

from hypothesis import given, strategies as st, settings, HealthCheck


def fake_sample_n(n, model, tokenizer, max_length, temperature):
    return [f"w{i}" for i in range(n)]


@given(n=st.integers(min_value=0, max_value=20), temp=st.floats(min_value=0.0, max_value=2.0))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_generated_properties(n, temp):
    # Monkeypatch at test time instead of using pytest's fixture
    orig_sample = appmod.sample_n
    try:
        appmod.sample_n = fake_sample_n
        resp = client.get(f"/generate?num_words={n}&temperature={temp}")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == n
        for w in data:
            assert isinstance(w, str)
            assert len(w) <= 20
    finally:
        appmod.sample_n = orig_sample
