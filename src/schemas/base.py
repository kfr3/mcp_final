from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True 