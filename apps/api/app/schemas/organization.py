import uuid

from pydantic import BaseModel, Field


class OrganizationOut(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    role: str

    class Config:
        from_attributes = True


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
