from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (add_request, delete_request, retrieve_request,
                                 retrieve_requests, update_request)
from app.server.models.request import (ErrorResponseModel, RequestSchema,
                                       RequestUpdateSchema, ResponseModel)

router = APIRouter()


@router.post(
    "/", response_description="Request data added into the database", status_code=201
)
async def add_request_data(request: RequestSchema = Body(...)):
    request = jsonable_encoder(request)
    new_request = await add_request(request)
    return ResponseModel(new_request, "Request added successfully.")


@router.get("/", response_description="Requests retrieved")
async def get_requests():
    requests = await retrieve_requests()
    if requests:
        return ResponseModel(requests, "Requests data retrieved successfully")
    return ResponseModel(requests, "Empty list returned")


@router.get("/{id}", response_description="Request data retrieved")
async def get_request_data(id):
    request = await retrieve_request(id)
    if request:
        return ResponseModel(request, "Request data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Request doesn't exist.")


@router.put("/{id}")
async def update_request_data(id: str, req: RequestUpdateSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_request = await update_request(id, req)
    if updated_request:
        return ResponseModel(
            "Request with ID: {} name update is successful".format(id),
            "Request name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the request data.",
    )


@router.delete("/{id}", response_description="Request data deleted from the database")
async def delete_request_data(id: str):
    deleted_request = await delete_request(id)
    if deleted_request:
        return ResponseModel(
            "Request with ID: {} removed".format(id), "Request deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Request with id {0} doesn't exist".format(id)
    )
