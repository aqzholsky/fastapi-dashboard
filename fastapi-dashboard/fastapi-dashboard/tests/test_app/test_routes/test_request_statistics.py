from datetime import datetime, timedelta

import pytest
from pymongo import MongoClient
from starlette.testclient import TestClient

import app.server.mongo_db as database
from app.server.app import app as fastapi_app
from tests.factories import RequestFactory, RobotFactory, UserFactory
from tests.functions.mongo_actions import drop_collection, enrich_collection


class TestRequestRouter:
    @pytest.fixture(autouse=True)
    def db(self):
        mongo_client = MongoClient(database.MONGO_DETAILS)
        return mongo_client.admin

    @pytest.fixture
    def client(self, db):
        client = TestClient(fastapi_app)
        enrich_collection(db, "robot_collection", RobotFactory)
        yield client
        drop_collection(db, "robot_collection")
        drop_collection(db, "request_collection")

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
    def user_id(self, register_user):
        response = register_user
        return response.json()["id"]

    @pytest.fixture
    def robot_id(self, db):
        return str(getattr(db, "robot_collection").find_one()["_id"])

    @pytest.fixture(autouse=True)
    def enrich_db_monthly_data(self, db, user_id, robot_id):

        this_month_days = [
            datetime.today(),
            datetime.today() - timedelta(10),
            datetime.today() - timedelta(20),
            datetime.today() - timedelta(30),
        ]

        later_month_days = [
            datetime.today() - timedelta(10**2),
            datetime.today() - timedelta(20**2),
            datetime.today() - timedelta(30**2),
        ]

        for day in [*this_month_days, *later_month_days]:
            r = RequestFactory.create_batch(
                10, user_id=user_id, robot_id=robot_id, created_at=day
            )
            getattr(db, "request_collection").insert_many(r)

        return this_month_days

    def test_daily_requests_by_status(
        self, client, user_authentication_headers, robot_id
    ):
        request_data = RequestFactory.create()
        response = client.get(
            f"/request_statistics/daily_requests_by_status/{robot_id}",
            json=request_data,
            headers=user_authentication_headers,
        )

        print(response.json())
        assert response.status_code == 201

    def test_daily_requests_of_last_month(
        self, client, user_authentication_headers, robot_id
    ):
        request_data = RequestFactory.create()
        response = client.get(
            f"/request_statistics/daily_requests_of_last_month/{robot_id}",
            json=request_data,
            headers=user_authentication_headers,
        )

        print(response.json())
        assert response.status_code == 201
