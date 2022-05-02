import re
from datetime import datetime
from enum import Enum
from functools import reduce
from operator import add, mul
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, ValidationError, validator


class Status(str, Enum):
    NEW = "NEW"
    IN_PROCESS = "IN_PROCESS"
    DONE = "DONE"
    FAIL = "FAIL"


class RequestSchema(BaseModel):
    # required
    first_name: str = Field(...)
    last_name: str = Field(...)
    iin: str = Field(...)

    # read_only
    status: Optional[Status] = Field(None)
    result: str = Field(None)
    created_at: datetime = Field(None)

    # validators
    @validator("iin")
    def validate_iin(cls, iin: str) -> bool:
        def multiply(iin: str, weights: List[int]) -> int:
            result = reduce(add, map(lambda i: mul(*i), zip(map(int, iin), weights)))
            return result

        if not re.match(r"[0-9]{12}", iin):
            raise ValidationError("Invalid iin")

        w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        w2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
        check_sum = multiply(iin, w1) % 11
        if check_sum == 10:
            check_sum = multiply(iin, w2) % 11
        if check_sum != int(iin[-1]):
            raise ValidationError("Invalid iin")

        return iin

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "iin": "000101400100",
            }
        }


class RequestUpdateSchema(RequestSchema):
    first_name: str = Field(None)
    last_name: str = Field(None)
    iin: str = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "iin": "000101400100",
                "status": "NEW, IN_PROCESS, DONE, FAIL",
                "created_at": "2022-05-02 00:26:37.660141",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
