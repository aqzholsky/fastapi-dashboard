from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from app.server.models import (ErrorResponseModel, ResponseModel, Robot, User, RobotState)
from app.server.repository import (add_robot, delete_robot, get_current_user,
                                   retrieve_robot, retrieve_robots,
                                   update_robot)
from app.server.repository.robot import delete_robot

router = APIRouter()


@router.get("/", response_description="Companies retrieved")
async def get_robots(user: User = Depends(get_current_user)):
    requests = await retrieve_robots(
        {
            "company_id": user.company_id,
        }
    )
    if requests:
        return requests

    ErrorResponseModel("An error occurred.", 404, "Robot doesn't exist.")


@router.post(
    "/",
    response_description="Robot data added into the database",
    status_code=201,
    response_model=Robot,
)
async def add_robot_data(
    robot: Robot = Body(...), user: User = Depends(get_current_user)
):
    robot = jsonable_encoder(robot)
    robot["company_id"] = user.company_id
    if not robot.get("state"):
        robot["state"] = RobotState.STOPPED

    new_robot = await add_robot(robot)
    return new_robot


@router.get("/{id}", response_description="robot data retrieved")
async def get_robot_data(id, user: User = Depends(get_current_user)):
    robot = await retrieve_robot(
        id,
        {
            "company_id": user.company_id,
        },
    )
    if robot:
        return robot
    return ErrorResponseModel("An error occurred.", 404, "Robot doesn't exist.")


@router.put("/{id}")
async def update_robot_data(
    id: str,
    req: Robot = Body(...),
    user: User = Depends(get_current_user),
):
    robot = await retrieve_robot(
        id,
        {
            "company_id": user.company_id,
        },
    )
    if not robot:
        return ErrorResponseModel(
            "An error occurred",
            401,
            "You have no access to change data.",
        )

    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_robot = await update_robot(id, req)
    if updated_robot:
        return updated_robot
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the robot data.",
    )


@router.delete("/{id}", response_description="robot data deleted from the database")
async def delete_robot_data(id: str, user: User = Depends(get_current_user)):

    robot = await retrieve_robot(
        id,
        {
            "company_id": user.company_id,
        },
    )
    if not robot:
        return ErrorResponseModel(
            "An error occurred",
            401,
            "You have no access to change data.",
        )

    deleted_robot = await delete_robot(id)
    if deleted_robot:
        return ResponseModel(
            "robot with ID: {} removed".format(id), "Robot deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Robot with id {0} doesn't exist".format(id)
    )
