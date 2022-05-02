# Monkey patch
import app.server.database as database

database.COLLECTION_NAME = "test_request_collection"

import pytest
from pymongo import MongoClient
from starlette.testclient import TestClient

from app.server.app import app
from tests.functions.mongo_actions import drop_collection, enrich_collection


class TestRequestRouter:
    @pytest.fixture(autouse=True)
    def db(self):
        mongo_client = MongoClient(database.MONGO_DETAILS)
        return mongo_client.admin

    @pytest.fixture
    def client(self, db):
        client = TestClient(app)
        enrich_collection(db, "request_collection")
        yield client
        drop_collection(db, "request_collection")

    @pytest.fixture
    def id(self, db):
        return str(getattr(db, "request_collection").find_one()["_id"])

    def test_retrieve(self, client, id):
        response = client.get(
            f"/request/{id}",
        )
        assert response.status_code == 200
        actual = response.json()["data"][0]
        assert actual["id"] == id

    def test_list(self, client):
        response = client.get(
            "/request/",
        )
        assert response.status_code == 200
        actual = response.json()["data"]
        assert len(actual) != 0

    def test_update(self, client, id):
        response = client.put(
            f"/request/{id}",
            json={
                "last_name": "Jones",
            },
        )
        assert response.status_code == 200
        assert id in response.json()["data"][0]

    def test_delete(self, client, id):
        response = client.delete(
            f"/request/{id}",
            json={
                "last_name": "Jones",
            },
        )
        assert response.status_code == 200
        assert id in response.json()["data"][0]
