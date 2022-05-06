from .authentication import (Token, TokenData, User, UserInDB, UserLogin,
                             UserRegistration)
from .company import Company
from .request import RequestSchema, RequestSchemaList, RequestUpdateSchema, Status
from .request_statistics import DailyRequestsByStatus, DailyRequestsOfLastMonth
from .robot import Robot, RobotState
from .robot_starter import RobotStarter


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
