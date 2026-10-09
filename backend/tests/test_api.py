from fastapi.testclient import TestClient

from app.main import app
from app.schemas import Automaton

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_is_stubbed():
    response = client.post("/api/analyze", json={"regex": "a|b*"})
    assert response.status_code == 501


def test_analyze_validates_input():
    response = client.post("/api/analyze", json={"regex": ""})
    assert response.status_code == 422


def test_automaton_schema_accepts_epsilon():
    automaton = Automaton(
        type="NFA",
        states=[{"id": 0, "label": "q0"}, {"id": 1, "label": "q1"}],
        alphabet=["a"],
        transitions=[
            {"source": 0, "target": 1, "symbol": "a"},
            {"source": 1, "target": 0, "symbol": None},
        ],
        start=0,
        accepting=[1],
    )
    assert automaton.transitions[1].symbol is None
