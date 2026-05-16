from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.user import User
from backend.schemas.auth import TokenResponse, RegisterRequest
from backend.auth.jwt_handler import verify_password, hash_password, create_access_token
from backend.auth.dependencies import require_roles

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.email, "role": user.role})
    return TokenResponse(access_token=token, role=user.role, full_name=user.full_name, email=user.email)


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db),
             _: User = Depends(require_roles("admin", "super_admin"))):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already exists")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user); db.commit(); db.refresh(user)
    return {"id": user.id, "email": user.email, "role": user.role}