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


@app.post("/kvpairs/", response_model=schemas.Kvpair)
def create_kvpair(kvpair: schemas.KvpairCreate, db: Session = Depends(get_db)):
    db_kvpair = crud.get_kvpair(db, key=kvpair.key)
    if db_kvpair:
        raise HTTPException(status_code=400, detail="key already existed")
    return crud.create_kvpair(db, kvpair=kvpair)


@app.get("/kvpairs/{key}", response_model=schemas.Kvpair)
def read_kvpair(key: str, db: Session = Depends(get_db)):
    db_kvpair = crud.get_kvpair(db, key=key)
    if db_kvpair is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_kvpair
