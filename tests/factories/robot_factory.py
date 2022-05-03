import faker

faker = faker.Faker()

from tests.factories.base_factory import BaseFactory


class RobotFactory(BaseFactory):
    def generate_data(*args, **kwargs):
        return {
            "name": kwargs.get("unamesername") or faker.first_name(),
            "server_address": kwargs.get("server_address") or faker.ipv4(),
            "start_time": str(kwargs.get("start_time") or faker.date_time()),
            "end_time": str(kwargs.get("end_time") or faker.date_time()),
            "company_id": kwargs.get("company_id"),
        }
