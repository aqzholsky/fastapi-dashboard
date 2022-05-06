from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.server.mongo_db import robot_starter
from app.server.models import RobotStarter


async def set_robot_starter(starter: RobotStarter) -> dict:
    obj = await robot_starter.find_one({"robot_id": starter.robot_id})
    obj = await robot_starter.update_one(
        {"robot_id": starter.robot_id}, {"$set": {'state': starter.state}})
    return True
