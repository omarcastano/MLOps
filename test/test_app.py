import pytest
from app.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_predict_positive_class():
    response = client.post("/predict/", json={"text": "I'm very happy"})
    pred = response.json()
    assert response.status_code == 200
    assert pred["label"] == "positive"
    assert pred["score"] > 0.5


def test_predict_negative_class():
    response = client.post("/predict/", json={"text": "I'm very sad"})
    pred = response.json()
    assert response.status_code == 200
    assert pred["label"] == "negative"
    assert pred["score"] > 0.5
