from pydantic import BaseModel
from typing   import Optional


class Base(BaseModel):
    id  : int
    name: Optional[str]


class Brand(Base):
    ...


class Model(Base):
    ...


class Config(BaseModel):
    brand: Brand
    model: Model