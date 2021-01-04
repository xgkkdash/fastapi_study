from sqlalchemy.orm import Session

from models import models
from schemas import schemas


def get_detail(db: Session, id: int):
    return db.query(models.Detail).filter(models.Detail.id == id).first()


def create_detail(db: Session, detail: schemas.DetailCreate):
    # db_detail = models.Detail(detail.id, detail.description)
    db_detail = models.Detail()
    db_detail.id = detail.id
    db_detail.description = detail.description
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail
