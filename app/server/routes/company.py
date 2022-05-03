from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from app.server.models import Company, ErrorResponseModel, ResponseModel, User
from app.server.repository import (
    add_company,
    delete_company,
    get_current_user,
    retrieve_companies,
    retrieve_company,
    update_company,
)

router = APIRouter()


@router.get("/own", response_description="Companies retrieved")
async def get_own_company(user: User = Depends(get_current_user)):
    company = await retrieve_company(user.company_id)
    if company:
        return company

    ErrorResponseModel("An error occurred.", 404, "Company doesn't exist.")


@router.get("/", response_description="Companies retrieved")
async def get_companies(_: User = Depends(get_current_user)):
    requests = await retrieve_companies()
    if requests:
        return requests

    ErrorResponseModel("An error occurred.", 404, "Company doesn't exist.")


@router.post(
    "/",
    response_description="Company data added into the database",
    status_code=201,
    response_model=Company,
)
async def add_company_data(
    company: Company = Body(...), _: User = Depends(get_current_user)
):
    company = jsonable_encoder(company)
    new_company = await add_company(company)
    return new_company


@router.get("/{id}", response_description="Company data retrieved")
async def get_company_data(id, _: User = Depends(get_current_user)):
    company = await retrieve_company(id)
    if company:
        return company
    return ErrorResponseModel("An error occurred.", 404, "company doesn't exist.")


@router.put("/{id}")
async def update_company_data(
    id: str,
    req: Company = Body(...),
    _: User = Depends(get_current_user),
):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_company = await update_company(id, req)
    if updated_company:
        return updated_company
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the company data.",
    )


@router.delete("/{id}", response_description="Company data deleted from the database")
async def delete_company_data(id: str, _: User = Depends(get_current_user)):
    deleted_company = await delete_company(id)
    if deleted_company:
        return ResponseModel(
            "Company with ID: {} removed".format(id), "Company deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Company with id {0} doesn't exist".format(id)
    )
