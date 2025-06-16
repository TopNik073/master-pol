from pydantic import BaseModel, Field, EmailStr


class UserControlRequestSchema(BaseModel):
    name: str
    password: str | None = Field(None, min_length=6)
    email: EmailStr
