import random

import faker

from app.server.models import Status

faker = faker.Faker()

from tests.factories.base_factory import BaseFactory


class RequestFactory(BaseFactory):
    def generate_data(*args, **kwargs):
        return {
            "first_name": kwargs.get("first_name") or faker.first_name(),
            "last_name": kwargs.get("last_name") or faker.last_name(),
            "iin": kwargs.get("iin") or "010228500103",
            "status": kwargs.get("status")
            or random.choice(
                [
                    Status.DONE.value,
                    Status.NEW.value,
                    Status.IN_PROCESS.value,
                    Status.FAIL.value,
                ]
            ),
            "result": kwargs.get("result") or faker.url(),
            "user_id": kwargs.get("user_id"),
            "robot_id": kwargs.get("robot_id"),
        }
