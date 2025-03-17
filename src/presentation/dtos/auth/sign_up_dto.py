from pydantic import BaseModel, EmailStr, Field


class SignUpDTO(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, max_length=12, example="StrongPass123")
