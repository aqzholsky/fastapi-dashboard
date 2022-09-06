import faker

faker = faker.Faker()

from tests.factories.base_factory import BaseFactory


class UserFactory(BaseFactory):
    def generate_data(*args, **kwargs):
        return {
            "username": kwargs.get("username") or faker.user_name(),
            "email": kwargs.get("email") or faker.company_email(),
            "full_name": kwargs.get("full_name")
            or f"{faker.first_name()} {faker.last_name()}",
            "hashed_password": kwargs.get("hashed_password")
            or faker.md5(raw_output=False),
            "company_id": kwargs.get("company_id"),
        }
