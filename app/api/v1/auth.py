from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.services.auth_service import AuthService
from app.api.deps import get_db


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = AuthService.register_user(db, payload.email, payload.phone, payload.password)
    return {"data": {"userId": str(user.id), "status": user.status}}


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user, session, ws_token = AuthService.login_user(db, payload.identifier, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Set refresh cookie
    response.set_cookie(key="refresh_token", value=str(session.id), httponly=True, secure=True, samesite="strict")
    return {"data": {
    "sessionId": str(session.id),
    "userId": str(user.id),
    "roles": ["user"],
    "wsToken": ws_token,
    "mfaRequired": False
    }}