import asyncio
from datetime import datetime

import motor.motor_asyncio
from bson.objectid import ObjectId
from odmantic import AIOEngine

from app.server.models.request import Status

MONGO_DETAILS = "mongodb://admin:admin@localhost:27017"
COLLECTION_NAME = "request_collection"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

client.get_io_loop = asyncio.get_event_loop
engine = AIOEngine(motor_client=client)
database = client.admin
request_collection = database.get_collection(COLLECTION_NAME)

# helpers
def request_helper(request) -> dict:
    return {
        "id": str(request["_id"]),
        "first_name": request["first_name"],
        "last_name": request["last_name"],
        "iin": request["iin"],
        "status": request.get("status"),
        "result": request.get("result"),
        "created_at": request.get("created_at"),
    }


# Retrieve all requests present in the database
async def retrieve_requests():
    requests_list = []
    async for request in request_collection.find():
        requests_list.append(request_helper(request))
    return requests_list


# Add a new request into to the database
async def add_request(request_data: dict) -> dict:
    request_data.update(
        {
            "status": Status.NEW,
            "created_at": datetime.now(),
        }
    )

    request = await request_collection.insert_one(request_data)
    new_request = await request_collection.find_one({"_id": request.inserted_id})
    return request_helper(new_request)


# Retrieve a request with a matching ID
async def retrieve_request(id: str) -> dict:
    new_request = await request_collection.find_one({"_id": ObjectId(id)})
    if new_request:
        return request_helper(new_request)


# Update a request with a matching ID
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


# Delete a request from the database
async def delete_request(id: str):
    request = await request_collection.find_one({"_id": ObjectId(id)})
    if request:
        await request_collection.delete_one({"_id": ObjectId(id)})
        return True
