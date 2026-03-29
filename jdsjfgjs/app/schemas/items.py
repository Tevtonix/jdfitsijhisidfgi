from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    
    class Config:
        orm_mode = True