from pydantic import BaseModel, EmailStr, Field


class ResendConfirmationCodeDTO(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

