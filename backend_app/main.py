from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/details/", response_model=schemas.Detail)
def create_detail(detail: schemas.DetailCreate, db: Session = Depends(get_db)):
    db_detail = crud.get_detail(db, id=detail.id)
    if db_detail:
        raise HTTPException(status_code=400, detail="id already existed")
    return crud.create_detail(db, detail=detail)


@app.get("/details/{id}", response_model=schemas.Detail)
def read_detail(id: int, db: Session = Depends(get_db)):
    db_detail = crud.get_detail(db, id=id)
    if db_detail is None:
        raise HTTPException(status_code=404, detail="Id not found")
    return db_detail
