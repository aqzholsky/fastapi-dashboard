from datetime import datetime, timedelta
from app.server.mongo_db import request_collection

def help_daily_requests_of_last_month(statistics):
    result = []
    for i in statistics:
        result.append(
            {
            "date": i["_id"],
            "count": i["count"],
            }
        )

def help_daily_requests_by_status(statistics):
    result = []
    for i in statistics:
        result.append(
            {
            "status": i["_id"],
            "count": i["count"],
            }
        )

async def daily_requests_of_last_month(lookup={}):
    add_fields = {  
        "$addFields":{  
            "_id":0,
            "day": {"$dateToString":{"format":"%d.%m.%Y", "date":"$created_at"}},
        }
    }

    match = {
        "$match": {
            "created_at": {"$gte": (datetime.today() - timedelta(30)), "$lte": datetime.today()}
        }
    }

    group = {
        "$group" : {
            "_id": "$day", 
            "count":{"$sum":1}
        }
    }

    match["$match"].update(lookup)

    aggregation = request_collection.aggregate(pipeline=[
        add_fields,
        match,
        group
    ])

    result = []
    async for doc in aggregation:
        result.append(doc)

    return result

async def daily_requests_by_status(lookup={}):
    add_fields = {  
        "$addFields":{  
            "_id":0,
            "created_day": {"$dateToString":{"format":"%d.%m.%Y", "date":"$created_at"}},
        }
    }
    match = {
        "$match": {
            "$expr":{'$eq':["$created_day", datetime.today().strftime("%d.%m.%Y")]},
            "user_id": 1,
        }
    }
    group = {
        "$group" : {
            "_id": "$status", 
            "count":{"$sum":1}
        }
    }
    match["$match"].update(lookup)

    
    result = []
    async for doc in request_collection.aggregate(pipeline=[
        add_fields,
        match,
        group
    ]):
        result.append(doc)

    # async for doc in request_collection.count_documents(lookup):
    print(result, "----", await request_collection.count_documents(lookup), await request_collection.count_documents())
    
    return result
