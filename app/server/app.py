from fastapi import FastAPI

from app.server.routes import (AuthenticationRouter, CompanyRouter,
                               RequestRouter, RobotRouter, RequestStatisticsRouter)

app = FastAPI()

app.include_router(RequestRouter, tags=["Request"], prefix="/request")
app.include_router(
    AuthenticationRouter, tags=["Authentication"], prefix="/authentication"
)
app.include_router(CompanyRouter, tags=["Company"], prefix="/company")
app.include_router(RobotRouter, tags=["Robot"], prefix="/robot")
app.include_router(RequestStatisticsRouter, tags=["Request Statistics"], prefix="/request_statistics")
