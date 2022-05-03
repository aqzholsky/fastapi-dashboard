from fastapi import FastAPI

from app.server.routes import (AuthenticationRouter, CompanyRouter,
                               RequestRouter, RobotRouter)

app = FastAPI()

app.include_router(RequestRouter, tags=["Request"], prefix="/request")
app.include_router(
    AuthenticationRouter, tags=["Authentication"], prefix="/authentication"
)
app.include_router(CompanyRouter, tags=["Company"], prefix="/company")
app.include_router(RobotRouter, tags=["Robot"], prefix="/robot")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
