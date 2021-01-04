from sqlalchemy.orm import Session

from models import models
from schemas import schemas


def get_kvpair(db: Session, key: str):
    return db.query(models.Kvpair).filter(models.Kvpair.key == key).first()


def create_kvpair(db: Session, kvpair: schemas.KvpairCreate):
    # db_kvpair = models.Kvpair(kvpair.key, kvpair.value)
    db_kvpair = models.Kvpair()
    db_kvpair.key = kvpair.key
    db_kvpair.value = kvpair.value
    db.add(db_kvpair)
    db.commit()
    db.refresh(db_kvpair)
    return db_kvpair
