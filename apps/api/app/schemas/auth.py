import uuid

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    organization_name: str = Field(min_length=1, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True


class MeResponse(BaseModel):
    user: UserOut
    organizations: list["OrganizationOut"]


from app.schemas.organization import OrganizationOut  # noqa: E402

MeResponse.model_rebuild()
