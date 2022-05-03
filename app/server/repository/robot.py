from bson.errors import InvalidId
from bson.objectid import ObjectId

from app.server.mongo_db import robot_collection


def robot_helper(robot):
    return {
        "id": str(robot["_id"]),
        "name": robot.get("name"),
        "server_address": robot.get("server_address"),
        "start_time": str(robot.get("start_time")),
        "end_time": str(robot.get("end_time")),
        "company_id": robot.get("company_id"),
        "state": robot.get("state"),
    }


async def retrieve_robots(lookup={}) -> list:
    robot_list = []
    async for robot in robot_collection.find(lookup):
        robot_list.append(robot_helper(robot))
    return robot_list


async def add_robot(robot_data: dict) -> dict:
    robot = await robot_collection.insert_one(robot_data)
    new_robot = await robot_collection.find_one({"_id": robot.inserted_id})
    return robot_helper(new_robot)


async def retrieve_robot(id: str, lookup={}) -> dict:
    try:
        new_lookup = {"_id": ObjectId(id)}
        new_lookup.update(lookup)

        new_robot = await robot_collection.find_one(new_lookup)
        if new_robot:
            return robot_helper(new_robot)
    except InvalidId:
        return None


async def update_robot(id: str, data: dict):
    if len(data) < 1:
        return False
    robot = await robot_collection.find_one({"_id": ObjectId(id)})
    if robot:
        updated_robot = await robot_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_robot:
            return True
        return False


async def delete_robot(id: str):
    robot = await robot_collection.find_one({"_id": ObjectId(id)})
    if robot:
        await robot_collection.delete_one({"_id": ObjectId(id)})
        return True
