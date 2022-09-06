from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Goldman Sachs",
                "email": "doe@gmail.com",
                "phone": "+1 123 45 45 444",
                "address": "Some address",
            }
        }
