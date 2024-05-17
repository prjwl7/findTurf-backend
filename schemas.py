# schemas.py
from pydantic import BaseModel

class JerseyBase(BaseModel):
    team: str
    league: str
    type: str
    home_away_third: str
    size: str
    number_of_jerseys: int
    price: float
    customizable: bool
    discounted_price: float

class JerseyCreate(JerseyBase):
    pass

class JerseyResponse(JerseyBase):
    id: int

    class Config:
        orm_mode = True
