from src.app import app
from fastapi.testclient import TestClient
from src.etl import MyETL
import pandas as pd
import pytest


# test MyETL
class TestETL:
    @pytest.fixture
    def my_etl(self):
        db_host = "maria_db"
        etl = MyETL(table_name="titanic", db_host=db_host)
        return etl

    def test_get_table(self, my_etl):
        assert isinstance(my_etl.get_table(), pd.DataFrame)

    def test_get_data(self, my_etl):
        X_train, X_test, y_train, y_test = my_etl.get_data(["age"], ["class"], "survived")

        assert len(X_train) > 0
        assert len(X_test) > 0
        assert len(y_train) > 0
        assert len(y_test) > 0


client = TestClient(app)


def test_app():
    response = client.post("/predict/", json={"age": 9, "class": "Third"})
    pred = response.json()
    assert response.status_code == 200
