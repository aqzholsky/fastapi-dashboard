from fastapi import APIRouter, Body, Depends

from app.server.models import RobotStarter
from app.server.repository import get_robot_state, update_robot_state

router = APIRouter()


@router.get(
    "/{robot_id}",
    response_description="get robot state"
)
async def robot_state(robot_id: str):
    obj = await get_robot_state(robot_id)
    return obj


@router.post(
    "/",
    response_description="set robot state"
)
async def set_robot_state(starter: RobotStarter):
    return await update_robot_state(starter)
