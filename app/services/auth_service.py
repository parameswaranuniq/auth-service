import bcrypt, uuid, datetime
from sqlalchemy.orm import Session
from app.db import models
from app.core.config import settings
import jwt


class AuthService:
    @staticmethod
    def register_user(db: Session, email: str | None, phone: str | None, password: str):
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = models.User(email=email, phone=phone, password_hash=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    @staticmethod
    def login_user(db: Session, identifier: str, password: str):
        user = db.query(models.User).filter(
        (models.User.email == identifier) | (models.User.phone == identifier)
        ).first()
        if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return None, None
        session = models.Session(user_id=user.id,
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.REFRESH_TOKEN_EXP))
        db.add(session)
        db.commit()
        db.refresh(session)
        ws_token = jwt.encode({"sid": str(session.id)}, settings.JWT_SIGNING_KEY, algorithm=settings.JWT_ALG)
        return user, session, ws_token