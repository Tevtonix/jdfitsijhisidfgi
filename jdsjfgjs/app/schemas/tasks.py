from pydantic import BaseModel, constr
from typing import Optional

class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True