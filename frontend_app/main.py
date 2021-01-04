import requests
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import crud
from models import models
from schemas import schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/kvpairs/", response_model=schemas.KvpairDetail)
def create_kvpair(kvpair_detail: schemas.KvpairDetailCreate, db: Session = Depends(get_db)):
    db_kvpair = crud.get_kvpair(db, key=kvpair_detail.key)
    if db_kvpair:
        raise HTTPException(status_code=400, detail="key already existed")
    else:
        kvpair = schemas.KvpairCreate(key=kvpair_detail.key, value=kvpair_detail.value)
        if kvpair_detail.id:
            back_data = None
            backend_url = "http://backend:5000/details/"
            try:
                backend_response = requests.post(backend_url,
                                                 json={"id": kvpair_detail.id, "description": kvpair_detail.description})
                if backend_response.status_code == 200:
                    back_data = backend_response.json()
            except Exception as e:
                print(e)
            if back_data:
                front_result = crud.create_kvpair(db, kvpair=kvpair)
                final_result = schemas.KvpairDetail(key=front_result.key, value=front_result.value,
                                                    id=back_data['id'], description=back_data['description'])
                return final_result
            else:
                raise HTTPException(status_code=400, detail="insert id/description failed")
        else:
            front_result = crud.create_kvpair(db, kvpair=kvpair)
            final_result = schemas.KvpairDetail(key=front_result.key, value=front_result.value)
            return final_result


@app.get("/kvpairs/{key}", response_model=schemas.KvpairDetail)
def read_kvpair(key: str, id: Optional[int] = 0,  db: Session = Depends(get_db)):
    back_data = None
    if id:
        backend_url = "http://backend:5000/details/" + str(id)
        try:
            backend_response = requests.get(backend_url)
            if backend_response.status_code == 200:
                back_data = backend_response.json()
        except Exception as e:
            print(e)
    db_kvpair = crud.get_kvpair(db, key=key)
    if db_kvpair is None:
        raise HTTPException(status_code=404, detail="Key not found")
    else:
        final_result = schemas.KvpairDetail(key=db_kvpair.key, value=db_kvpair.value)
        if back_data:
            final_result.id = back_data['id']
            final_result.description = back_data['description']
        return final_result
