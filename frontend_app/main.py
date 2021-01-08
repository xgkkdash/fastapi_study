import asyncio
import aiohttp
import motor.motor_asyncio
import os
from typing import Optional

from fastapi import FastAPI, HTTPException

from models.kvpair import Kvpair
from schemas import schemas
from database.mongodb import find_kvpair, insert_kvpair

app = FastAPI()


# Dependency
def get_db():
    db_name = os.environ.get('DB_NAME', 'front_dev')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '27017')
    db_url = "mongodb://" + db_host + ":" + str(db_port) + "/"
    db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    return db_client[db_name]


db = get_db()


@app.post("/kvpairs/", response_model=schemas.KvpairDetail)
async def create_kvpair(kvpair_detail: schemas.KvpairDetailCreate):
    db_kvpair_doc = await find_kvpair(db, kvpair_detail.key)
    if db_kvpair_doc:
        raise HTTPException(status_code=400, detail="key already existed")
    else:
        if kvpair_detail.id:
            back_data = None
            backend_url = "http://backend:5000/details/"
            param_json = {"id": kvpair_detail.id, "description": kvpair_detail.description}
            async with aiohttp.ClientSession() as session:
                async with session.post(backend_url, json=param_json) as response:
                    if response.status == 200:
                        back_data = await response.json()
            if back_data:
                front_result = Kvpair(kvpair_detail.key, kvpair_detail.value)
                await insert_kvpair(db, front_result)
                final_result = schemas.KvpairDetail(key=front_result.key, value=front_result.value,
                                                    id=back_data['id'], description=back_data['description'])
                return final_result
            else:
                raise HTTPException(status_code=400, detail="insert id/description failed")
        else:
            front_result = Kvpair(kvpair_detail.key, kvpair_detail.value)
            await insert_kvpair(db, front_result)
            final_result = schemas.KvpairDetail(key=front_result.key, value=front_result.value)
            return final_result


@app.get("/kvpairs/{key}", response_model=schemas.KvpairDetail)
async def read_kvpair(key: str, id: Optional[int] = 0):
    # TODO: use asyncio.tasks instead of run_in_executor to concurrently get db_kvpair and back_data
    back_data = None
    if id:
        backend_url = "http://backend:5000/details/" + str(id)
        async with aiohttp.ClientSession() as session:
            async with session.get(backend_url) as response:
                if response.status == 200:
                    back_data = await response.json()
    db_kvpair_doc = await find_kvpair(db, key)
    if db_kvpair_doc is None:
        raise HTTPException(status_code=404, detail="Key not found")
    else:
        db_kvpair_doc.pop('_id')
        db_kvpair = Kvpair(**db_kvpair_doc)
        final_result = schemas.KvpairDetail(key=db_kvpair.key, value=db_kvpair.value)
        if back_data:
            final_result.id = back_data['id']
            final_result.description = back_data['description']
        return final_result
