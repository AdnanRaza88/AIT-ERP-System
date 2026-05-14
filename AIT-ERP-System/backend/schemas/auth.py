from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str
    email: EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "student"