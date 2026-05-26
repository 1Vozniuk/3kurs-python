from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    user_id: int
    bio: Optional[str] = Field(default=None, max_length=500)
    phone: Optional[str] = Field(default=None, max_length=30)


class ProfileOut(ProfileCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
