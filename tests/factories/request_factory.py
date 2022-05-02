import faker

faker = faker.Faker()


class RequestFactory:
    def __generate_data(first_name, last_name, iin):
        return {
            "first_name": first_name or faker.first_name(),
            "last_name": last_name or faker.last_name(),
            "iin": iin or str(faker.pydecimal(positive=True, right_digits=0)),
        }
        pass

    @classmethod
    def create(
        cls,
        first_name=None,
        last_name=None,
        iin=None,
    ):
        return cls.__generate_data(first_name, last_name, iin)

    @classmethod
    def create_batch(cls, first_name=None, last_name=None, iin=None, count=1):
        result = []
        for _ in range(count):
            result.append(cls.__generate_data(first_name, last_name, iin))
        return result
