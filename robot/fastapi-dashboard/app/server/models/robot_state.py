from pydantic import BaseModel


class RobotStarter(BaseModel):
    robot_id: str
    state: str