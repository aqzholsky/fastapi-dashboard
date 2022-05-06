from fastapi import APIRouter, Body, Depends

from app.server.models import RobotStarter
from app.server.repository import set_robot_starter

router = APIRouter()


@router.post(
    "/robot_id"
)
async def set_robot_start(starter: RobotStarter):
    return await set_robot_starter(starter)
