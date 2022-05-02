import random

from tests.factories.request_factory import RequestFactory


def enrich_collection(db, collection_name):
    getattr(db, collection_name).insert_many(
        RequestFactory.create_batch(count=random.randint(10, 20))
    )


def drop_collection(db, collection_name):
    db.get_collection(collection_name).drop()
