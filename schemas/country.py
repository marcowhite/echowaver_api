from pydantic import BaseModel
from typing import Optional

class SCountryAdd(BaseModel):
    name: str
    code: str

class SCountry(SCountryAdd):
    id: int