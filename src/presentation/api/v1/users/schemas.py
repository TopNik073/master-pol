from pydantic import BaseModel, EmailStr, Field


class UserControlRequestSchema(BaseModel):
    name: str
    password: str | None = Field(None, min_length=6)
    email: EmailStr
