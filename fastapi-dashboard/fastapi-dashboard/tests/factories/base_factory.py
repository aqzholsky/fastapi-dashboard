class BaseFactory:
    @classmethod
    def create(cls, *args, **kwargs):
        return cls.generate_data(*args, **kwargs)

    @classmethod
    def create_batch(cls, *args, **kwargs):
        result = []
        count = args[0] if args else 1
        for _ in range(count):
            result.append(cls.generate_data(*args, **kwargs))
        return result
