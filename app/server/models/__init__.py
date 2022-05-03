from .authentication import (Token, TokenData, User, UserInDB, UserLogin,
                             UserRegistration)
from .company import Company
from .request import RequestSchema, RequestUpdateSchema, Status
from .robot import Robot, RobotState


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
