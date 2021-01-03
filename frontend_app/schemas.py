from pydantic import BaseModel


class KvpairBase(BaseModel):
    key: str
    value: str


class KvpairCreate(KvpairBase):
    pass


class Kvpair(KvpairBase):

    class Config:
        orm_mode = True
