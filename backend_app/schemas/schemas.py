from pydantic import BaseModel


class DetailBase(BaseModel):
    id: int
    description: str


class DetailCreate(DetailBase):
    pass


class Detail(DetailBase):

    class Config:
        orm_mode = True
