# auth_service.py

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import User
from schemas import TokenData

# Ключ для підпису та перевірки токенів
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.execute(select(User).where(User.username == token_data.username))
    db_user = user.scalar_one_or_none()
    if db_user is None:
        raise credentials_exception
    return db_user
from fastapi import HTTPException

async def send_verification_email(email: str, verification_token: str):
    # Відправка листа з посиланням для підтвердження
    print(f"Sending verification email to {email} with token {verification_token}")

async def verify_email(token: str):
    # Перевірка токена і позначення користувача як верифікованого
    if token != "valid_token":
        raise HTTPException(status_code=400, detail="Invalid verification token")
