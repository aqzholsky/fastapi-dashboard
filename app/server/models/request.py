import re
from datetime import datetime
from enum import Enum
from functools import reduce
from operator import add, mul
from tkinter.messagebox import NO
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, validator


class Status(str, Enum):
    NEW = "NEW"
    IN_PROCESS = "IN_PROCESS"
    DONE = "DONE"
    FAIL = "FAIL"


class RequestSchema(BaseModel):
    id: Optional[str] = None
    first_name: Optional[str] = Field(...)
    last_name: Optional[str] = Field(...)
    iin: Optional[str] = Field(...)
    robot_id: Optional[str] = Field(...)
    service_name: Optional[str] = Field(...)

    status: Optional[Status] = None
    result: Optional[str] = None
    created_at: Optional[datetime] = None
    user_id: Optional[str] = None

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
                "service_name": "GET ADDRESS",
                "robot_id": "d0055d544c84e4b23438d0055d544c84e4b23438",
            }
        }


class RequestUpdateSchema(RequestSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    iin: Optional[str] = None
    robot_id: Optional[str] = None
    service_name: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "iin": "000101400100",
                "status": "NEW, IN_PROCESS, DONE, FAIL",
                "robot_id": "d0055d544c84e4b23438d0055d544c84e4b23438",
            }
        }
