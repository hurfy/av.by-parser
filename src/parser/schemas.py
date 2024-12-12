from pydantic import BaseModel, Field, HttpUrl
from enum     import Enum


class CarPrice(BaseModel):
    byn: int = Field(gt=0)
    usd: int = Field(gt=0)


class Car(BaseModel):
    model : str = Field(max_length=256)
    params: str = Field(max_length=512)
    price : CarPrice
    url   : HttpUrl


# Soon... (maybe)
class GearBoxType(str, Enum):
    AUTOMATIC  = "automatic"
    MECHANICAL = "mechanical"


class CarBase(BaseModel):
    brand: str
    model: str
    extra: str | None


class CarEngine(BaseModel):
    type  : str
    volume: float


class CarParameters(BaseModel):
    year    : int = Field(ge=1900, lt=2100)
    gear_box: GearBoxType
