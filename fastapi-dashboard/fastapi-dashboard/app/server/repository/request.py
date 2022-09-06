from datetime import datetime

from bson.errors import InvalidId
from bson.objectid import ObjectId

from app.server.mongo_db import request_collection


def request_helper(request) -> dict:
    return {
        "id": str(request["_id"]),
        "first_name": request["first_name"],
        "last_name": request["last_name"],
        "iin": request["iin"],
        "service_name": request.get("service_name"),
        "status": request.get("status"),
        "result": request.get("result"),
        "created_at": request.get("created_at"),
        "robot_id": request.get("robot_id"),
    }


async def retrieve_requests(lookup={}):
    requests_list = []
    async for request in request_collection.find(lookup):
        requests_list.append(request_helper(request))
    return requests_list


async def add_request(request_data: dict) -> dict:
    request_data["created_at"] = datetime.now()
    request = await request_collection.insert_one(request_data)
    new_request = await request_collection.find_one({"_id": request.inserted_id})
    return request_helper(new_request)


async def bulk_insert(requests: list):
    created_at = datetime.now()
    for r in requests:
        r["created_at"] = created_at
    await request_collection.insert_many(requests)

    new_requests = []
    async for request in request_collection.find({"created_at": created_at}):
        new_requests.append(request_helper(request))
    return new_requests


async def retrieve_request(id: str, lookup={}) -> dict:
    try:
        new_lookup = {"_id": ObjectId(id)}
        new_lookup.update(lookup)
        new_request = await request_collection.find_one(new_lookup)
        if new_request:
            return request_helper(new_request)
    except InvalidId:
        return None


async def update_request(id: str, data: dict):
    if len(data) < 1:
        return False
    request = await request_collection.find_one({"_id": ObjectId(id)})
    if request:
        updated_request = await request_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_request:
            return True
        return False


async def delete_request(id: str):
    request = await request_collection.find_one({"_id": ObjectId(id)})
    if request:
        await request_collection.delete_one({"_id": ObjectId(id)})
        return True
