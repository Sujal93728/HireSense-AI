from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from .database import SessionLocal
from . import crud

# ==========================================
# JWT Configuration
# ==========================================

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ==========================================
# Password Hashing
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# ==========================================
# OAuth2
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ==========================================
# Database Dependency
# ==========================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# Create JWT Token
# ==========================================

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==========================================
# Decode JWT & Get Current User
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    print("\n" + "=" * 60)
    print("AUTHENTICATION STARTED")
    print("=" * 60)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    print("Received Token:")
    print(token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("\nDecoded Payload:")
        print(payload)

        email = payload.get("sub")

        print("\nEmail from Token:")
        print(email)

        if email is None:
            print("ERROR: 'sub' claim missing")
            raise credentials_exception

    except JWTError as e:
        print("\nJWT ERROR:")
        print(e)
        raise credentials_exception

    print("\nSearching user in database...")

    user = crud.get_user_by_email(
        db,
        email
    )

    print("Database User:")
    print(user)

    if user is None:
        print("ERROR: User not found")
        raise credentials_exception

    print("\nAUTHENTICATION SUCCESSFUL")
    print("=" * 60)

    return user