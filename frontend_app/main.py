import asyncio
import functools
import os
import requests
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException

from models.kvpair import Kvpair
from schemas import schemas
from database.mongodb import MongoDatabase

app = FastAPI()


# Dependency
def get_db():
    db_name = os.environ.get('DB_NAME', 'front_dev')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '27017')
    db_url = "mongodb://" + db_host + ":" + str(db_port) + "/"
    db = MongoDatabase(db_name, db_url)
    yield db


@app.post("/kvpairs/", response_model=schemas.KvpairDetail)
async def create_kvpair(kvpair_detail: schemas.KvpairDetailCreate, db=Depends(get_db)):
    loop = asyncio.get_event_loop()
    db_kvpair = await loop.run_in_executor(None, db.get_kvpair, kvpair_detail.key)
    if db_kvpair:
        raise HTTPException(status_code=400, detail="key already existed")
    else:
        if kvpair_detail.id:
            back_data = None
            backend_url = "http://backend:5000/details/"
            try:
                param_json = {"id": kvpair_detail.id, "description": kvpair_detail.description}
                backend_response = await loop.run_in_executor(None, functools.partial(requests.post, url=backend_url,
                                                                                      json=param_json))
                if backend_response.status_code == 200:
                    back_data = backend_response.json()
            except Exception as e:
                print(e)
            if back_data:
                front_result = Kvpair(kvpair_detail.key, kvpair_detail.value)
                loop.run_in_executor(None, db.save_kvpair, front_result)
                final_result = schemas.KvpairDetail(key=front_result.key, value=front_result.value,
                                                    id=back_data['id'], description=back_data['description'])
                return final_result
            else:
                raise HTTPException(status_code=400, detail="insert id/description failed")
        else:
            front_result = Kvpair(kvpair_detail.key, kvpair_detail.value)
            loop.run_in_executor(None, db.save_kvpair, front_result)
            final_result = schemas.KvpairDetail(key=front_result.key, value=front_result.value)
            return final_result


@app.get("/kvpairs/{key}", response_model=schemas.KvpairDetail)
async def read_kvpair(key: str, id: Optional[int] = 0,  db=Depends(get_db)):
    loop = asyncio.get_event_loop()
    # TODO: use asyncio.tasks instead of run_in_executor to concurrently get db_kvpair and back_data
    back_data = None
    if id:
        backend_url = "http://backend:5000/details/" + str(id)
        try:
            backend_response = await loop.run_in_executor(None, requests.get, backend_url)
            if backend_response.status_code == 200:
                back_data = backend_response.json()
        except Exception as e:
            print(e)
    db_kvpair = await loop.run_in_executor(None, db.get_kvpair, key)
    if db_kvpair is None:
        raise HTTPException(status_code=404, detail="Key not found")
    else:
        final_result = schemas.KvpairDetail(key=db_kvpair.key, value=db_kvpair.value)
        if back_data:
            final_result.id = back_data['id']
            final_result.description = back_data['description']
        return final_result
