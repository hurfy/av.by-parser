from pydantic import BaseModel


class Base(BaseModel):
    id  : int
    name: str | None


class Brand(Base):
    ...


class Model(Base):
    ...


class Config(BaseModel):
    brand: Brand
    model: Model
