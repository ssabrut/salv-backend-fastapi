from . import *


class UserIn(BaseModel):
    id: str
    type_id: str
    name: str
    username: str
    password: str
    phone_number: str
    point: int
    province: str
    city: str
    subdistrict: str
    ward: str
    address: str
    postal_code: str
    image: str | None = ""
    latitude: float
    longitude: float
    created_at: str | None = datetime.now()
    updated_at: str | None = None


class UserOut(BaseModel):
    id: str
    type_id: str
    name: str
    username: str
    phone_number: str
    point: int
    province: str
    city: str
    subdistrict: str
    ward: str
    address: str
    postal_code: str
    image: str | None = ""
    latitude: float
    longitude: float
