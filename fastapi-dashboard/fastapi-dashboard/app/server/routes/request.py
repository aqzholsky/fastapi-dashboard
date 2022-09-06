import copy
import io
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, List

import pandas
import pandas as pd
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from app.server.models import (ErrorResponseModel, RequestSchema,
                               RequestSchemaList, RequestUpdateSchema,
                               ResponseModel, Status, User)
from app.server.repository import (add_request, bulk_insert, delete_request,
                                   get_current_user, retrieve_request,
                                   retrieve_requests, update_request)

router = APIRouter()


@router.post(
    "/",
    response_description="Request data added into the database",
    status_code=201,
    response_model=RequestSchema,
)
async def add_request_data(
    request: RequestSchema = Body(...), user: User = Depends(get_current_user)
):
    request = jsonable_encoder(request)
    request["user_id"] = user.id

    if not request.get("status"):
        request["status"] = Status.NEW

    new_request = await add_request(request)
    return new_request


@router.get("/get_report/{robot_id}")
async def get_report(robot_id, user: User = Depends(get_current_user)):
    def remove_keys(data):
        title = ['first_name', 'last_name', 'iin', 'status']

        data_copy = copy.copy(data)
        for key in data_copy:
            if key not in title:
                del data[key]
        return data

    requests = await retrieve_requests({
        "robot_id": robot_id
    })

    requests = list(map(remove_keys, requests))

    df = pandas.DataFrame(requests)
    stream = io.StringIO()
    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response


@router.post(
    "/bulk_create",
    response_description="Request data added into the database",
    status_code=201,
    response_model=List[RequestSchema],
)
async def insert_file_data(
    robot_id: str, file: UploadFile, user: User = Depends(get_current_user)
):
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        file.file.close()

    try:
        if suffix == ".xlsx":
            requests_df = pd.read_excel(tmp_path, sheet_name=0, dtype=str)
        elif suffix == ".csv":
            requests_df = pd.read_csv(
                tmp_path, encoding="utf-8", delimiter=";", dtype=str
            )
            requests_df = requests_df.dropna(axis=0)
        else:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Неправильный тип файла",
            )

        requests_df["robot_id"] = robot_id
        requests_df["user_id"] = user.id
        requests_df["status"] = Status.NEW
        requests = requests_df.to_dict("records")

        requests = RequestSchemaList(__root__=requests)
        requests = jsonable_encoder(requests)
        return await bulk_insert(requests)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильные имена колонок"
        )


@router.get("/", response_description="Requests retrieved")
async def get_requests(user: User = Depends(get_current_user)):
    requests = await retrieve_requests(
        {
            "user_id": user.id,
        }
    )
    if requests:
        return requests

    ErrorResponseModel("An error occurred.", 404, "Request doesn't exist.")


@router.get("/robot/{robot_id}", response_description="Requests retrieved")
async def get_robot_requests(robot_id, user: User = Depends(get_current_user)):
    requests = await retrieve_requests(
        {
            # "user_id": user.id,
            "robot_id": robot_id,
        }
    )
    if requests:
        return requests[:100]

    ErrorResponseModel("An error occurred.", 404, "Request doesn't exist.")


@router.get("/{id}", response_description="Request data retrieved")
async def get_request_data(id, user: User = Depends(get_current_user)):
    request = await retrieve_request(
        id,
        {
            "user_id": user.id,
        },
    )
    if request:
        return request
    return ErrorResponseModel("An error occurred.", 404, "Request doesn't exist.")


@router.put("/{id}")
async def update_request_data(
    id: str,
    req: RequestUpdateSchema = Body(...),
    user: User = Depends(get_current_user),
):
    request = await retrieve_request(id, {"user_id": user.id})
    if not request:
        return ErrorResponseModel(
            "An error occurred",
            401,
            "You have no access to change data.",
        )

    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_request = await update_request(id, req)
    if updated_request:
        return updated_request
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the request data.",
    )


@router.delete("/{id}", response_description="Request data deleted from the database")
async def delete_request_data(id: str, user: User = Depends(get_current_user)):
    request = await retrieve_request(id, {"user_id": user.id})
    if not request:
        return ErrorResponseModel(
            "An error occurred",
            401,
            "You have no access to change data.",
        )

    deleted_request = await delete_request(id)
    if deleted_request:
        return ResponseModel(
            "Request with ID: {} removed".format(id), "Request deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Request with id {0} doesn't exist".format(id)
    )
