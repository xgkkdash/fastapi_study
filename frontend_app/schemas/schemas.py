from pydantic import BaseModel


class KvpairBase(BaseModel):
    key: str
    value: str


class KvpairCreate(KvpairBase):
    pass


class Kvpair(KvpairBase):

    class Config:
        orm_mode = True


class KvpairDetailBase(KvpairBase):
    id: int = 0
    description: str = None


class KvpairDetailCreate(KvpairDetailBase):
    pass


class KvpairDetail(KvpairDetailBase):

    class Config:
        orm_mode = True
