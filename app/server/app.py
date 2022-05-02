from fastapi import FastAPI

from app.server.routes.request import router as RequestRouter

app = FastAPI()

app.include_router(RequestRouter, tags=["Request"], prefix="/request")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/ping")
def pong():
    return {"ping": "pong!"}
