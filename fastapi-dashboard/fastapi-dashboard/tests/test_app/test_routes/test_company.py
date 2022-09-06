import pytest
from pymongo import MongoClient
from starlette.testclient import TestClient

import app.server.mongo_db as database
from app.server.app import app as fastapi_app
from tests.factories import CompanyFactory, UserFactory
from tests.functions.mongo_actions import drop_collection, enrich_collection


class TestCompanyRouter:
    @pytest.fixture(autouse=True)
    def db(self):
        mongo_client = MongoClient(database.MONGO_DETAILS)
        return mongo_client.admin

    @pytest.fixture
    def client(self, db):
        client = TestClient(fastapi_app)
        enrich_collection(db, "company_collection", CompanyFactory)
        yield client
        drop_collection(db, "company_collection")

    @pytest.fixture
    def user(self, db):
        user = UserFactory.create()
        getattr(db, "user_collection").delete_one({"username": user["username"]})
        user["password1"] = user["hashed_password"]
        user["password2"] = user["hashed_password"]
        del user["hashed_password"]
        return user

    @pytest.fixture(autouse=True)
    def register_user(self, client, user):
        response = client.post("/authentication/register", json=user)
        assert response.status_code == 200
        return response

    @pytest.fixture(autouse=True)
    def user_authentication_headers(self, client, user):
        response = client.post(
            "/authentication/token",
            json={
                "username": user["username"],
                "password": user["password1"],
            },
        )
        assert response.status_code == 200
        access_token = response.json()["access_token"]
        return {"Authorization": f"Bearer {access_token}"}

    @pytest.fixture
    def id(self, db):
        return str(getattr(db, "company_collection").find_one()["_id"])

    def test_create(self, client, user_authentication_headers):
        company_data = CompanyFactory.create()
        response = client.post(
            f"/company/", json=company_data, headers=user_authentication_headers
        )

        actual = response.json()
        for key, value in company_data.items():
            assert actual[key] == value
        assert response.status_code == 201

    def test_retrieve_own(self, client, user_authentication_headers):
        response = client.get(f"/company/own", headers=user_authentication_headers)
        assert response.status_code == 200

    def test_retrieve(self, client, id, user_authentication_headers):
        response = client.get(f"/company/{id}", headers=user_authentication_headers)
        assert response.status_code == 200
        actual = response.json()
        assert actual["id"] == id

    def test_list(self, client, user_authentication_headers):
        response = client.get("/company/", headers=user_authentication_headers)
        assert response.status_code == 200
        actual = response.json()
        assert len(actual) != 0

    def test_update(self, client, id, user_authentication_headers):
        response = client.put(
            f"/company/{id}",
            json={
                "email": "a@a.vom",
            },
            headers=user_authentication_headers,
        )
        assert response.status_code == 200
        assert response.json()

    def test_delete(self, client, id, user_authentication_headers):
        response = client.delete(
            f"/company/{id}",
            headers=user_authentication_headers,
        )
        assert response.status_code == 200
        assert id in response.json()["data"][0]
