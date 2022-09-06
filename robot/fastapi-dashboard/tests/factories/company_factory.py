import faker

faker = faker.Faker()

from tests.factories.base_factory import BaseFactory


class CompanyFactory(BaseFactory):
    def generate_data(*args, **kwargs):
        return {
            "name": kwargs.get("name") or faker.first_name(),
            "email": kwargs.get("email") or faker.company_email(),
            "phone": kwargs.get("phone") or faker.phone_number(),
            "address": kwargs.get("address") or faker.address(),
        }
