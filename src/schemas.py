from pydantic import BaseModel

from typing import Sequence


class Boss(BaseModel):
    id: int
    name: str
    location: str


class BossSearchResults(BaseModel):
    results: Sequence[Boss]


class BossCreate(BaseModel):
    name: str
    location: str
