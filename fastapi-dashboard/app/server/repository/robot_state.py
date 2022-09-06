from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.server.mongo_db import robot_starter
from app.server.models import RobotStarter


def robot_state_helper(robot_state):
    return {
        "id": str(robot_state["_id"]),
        "state": robot_state.get("state"),
        "robot_id": robot_state.get("robot_id")
    }


async def get_robot_state(robot_id: str) -> dict:
    obj = await robot_starter.find_one({"robot_id": robot_id})
    return robot_state_helper(obj)


async def update_robot_state(starter: RobotStarter) -> bool:
    robot = await robot_starter.find_one({"robot_id": starter.robot_id})
    if robot:
        robot = await robot_starter.update_one(
            {"robot_id": starter.robot_id}, {"$set": {"state": starter.state}})
        if robot:
            return True
    return False
