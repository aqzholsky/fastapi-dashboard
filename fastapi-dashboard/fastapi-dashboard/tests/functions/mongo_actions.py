import random


def enrich_collection(db, collection_name, factory, fields={}):
    getattr(db, collection_name).insert_many(
        factory.create_batch(count=random.randint(10, 20), **fields)
    )


def drop_collection(db, collection_name):
    db.get_collection(collection_name).drop()
