from bson.errors import InvalidId
from bson.objectid import ObjectId

from app.server.mongo_db import company_collection
from tests.factories.company_factory import CompanyFactory


def company_helper(company):
    return {
        "id": str(company.get("_id")),
        "name": company.get("name"),
        "email": company.get("email"),
        "phone": company.get("phone"),
        "address": company.get("address"),
    }


async def retrieve_companies() -> list:
    company_list = []
    async for company in company_collection.find():
        company_list.append(company_helper(company))
    return company_list


async def add_company(company_data: dict) -> dict:
    company = await company_collection.insert_one(company_data)
    new_company = await company_collection.find_one({"_id": company.inserted_id})
    return company_helper(new_company)


async def retrieve_company(id: str) -> dict:
    try:
        new_company = await company_collection.find_one({"_id": ObjectId(id)})
        if new_company:
            return company_helper(new_company)
    except InvalidId:
        return None


async def retrieve_random_company() -> dict:
    random_company = await company_collection.find_one()
    if not random_company:
        return await add_company(CompanyFactory.create())
    return company_helper(random_company)


async def update_company(id: str, data: dict):
    if len(data) < 1:
        return False
    company = await company_collection.find_one({"_id": ObjectId(id)})
    if company:
        updated_company = await company_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_company:
            return True
        return False


async def delete_company(id: str):
    company = await company_collection.find_one({"_id": ObjectId(id)})
    if company:
        await company_collection.delete_one({"_id": ObjectId(id)})
        return True
