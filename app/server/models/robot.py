from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Robot(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    server_address: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    company_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Goldman Sachs",
                "server_address": "127.0.0.1",
                "start_time": "2022-05-03 15:06:08.856999",
                "end_time": "2022-05-03 15:06:08.856999",
                "company_id": "company_id",
            }
        }
