from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.server.routes import (AuthenticationRouter, CompanyRouter,
                               RequestRouter, RequestStatisticsRouter,
                               RobotRouter, RobotStarterRouter)

app = FastAPI()

app.include_router(RequestRouter, tags=["Request"], prefix="/request")
app.include_router(
    AuthenticationRouter, tags=["Authentication"], prefix="/authentication"
)
app.include_router(CompanyRouter, tags=["Company"], prefix="/company")
app.include_router(RobotRouter, tags=["Robot"], prefix="/robot")
app.include_router(
    RequestStatisticsRouter, tags=["Request Statistics"], prefix="/request_statistics"
)
app.include_router(RequestStatisticsRouter, tags=["Request Statistics"], prefix="/request_statistics")
app.include_router(RobotStarterRouter, tags=["Robot Starter"], prefix="/robot_starter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
