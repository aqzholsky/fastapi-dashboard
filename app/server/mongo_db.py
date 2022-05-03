import asyncio

import motor.motor_asyncio
from odmantic import AIOEngine

MONGO_DETAILS = "mongodb://admin:admin@localhost:27017"

REQUEST_COLLECTION_NAME = "request_collection"
USER_COLLECTION_NAME = "user_collection"
COMPANY_COLLECTION_NAME = "company_collection"
ROBOT_COLLECTION_NAME = "robot_collection"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

client.get_io_loop = asyncio.get_event_loop
engine = AIOEngine(motor_client=client)
database = client.admin

request_collection = database.get_collection(REQUEST_COLLECTION_NAME)
user_collection = database.get_collection(USER_COLLECTION_NAME)
company_collection = database.get_collection(COMPANY_COLLECTION_NAME)
robot_collection = database.get_collection(ROBOT_COLLECTION_NAME)
