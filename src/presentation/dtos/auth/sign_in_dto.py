from pydantic import BaseModel, EmailStr, Field


class SignInDTO(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, max_length=20, example="StrongPass123")

