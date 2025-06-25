from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    user_id: int
    item_name: str
    quantity: int

class OrderUpdate(BaseModel):
    item_name: Optional[str]
    quantity: Optional[int]
    status: Optional[str]

class OrderOut(BaseModel):
    id: int
    user_id: int
    item_name: str
    quantity: int
    status: str

    class Config:
        from_attributes = True
