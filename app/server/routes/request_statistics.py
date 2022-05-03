from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from app.server.models import (
    ErrorResponseModel,
    User,
)

from app.server.repository import (
    get_current_user,
    help_daily_requests_by_status,
    help_daily_requests_of_last_month,
    daily_requests_by_status,
    daily_requests_of_last_month,
)

from app.server.models import (
    DailyRequestsByStatus,
    DailyRequestsOfLastMonth,
)

router = APIRouter()


@router.get(
    "/daily_requests_by_status/{robot_id}",
    response_description="Requests retrieved",
    response_model=List[DailyRequestsByStatus],
)
async def get_daily_requests_by_status(
    robot_id, user: User = Depends(get_current_user)
):
    requests = await daily_requests_by_status(
        {
            # "user_id": user._id,
            "robot_id": robot_id,
        }
    )
    if requests:
        return help_daily_requests_by_status(requests)

    ErrorResponseModel("An error occurred.", 404, "Request doesn't exist.")


@router.get(
    "/daily_requests_of_last_month/{robot_id}",
    response_description="Requests retrieved",
    response_model=List[DailyRequestsOfLastMonth],
)
async def get_daily_requests_of_last_month(
    robot_id, user: User = Depends(get_current_user)
):
    requests = await daily_requests_of_last_month(
        {
            # "user_id": user._id,
            "robot_id": robot_id,
        }
    )
    if requests:
        return help_daily_requests_of_last_month(requests)

    ErrorResponseModel("An error occurred.", 404, "Request doesn't exist.")
