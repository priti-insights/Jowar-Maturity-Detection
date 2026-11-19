
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import mysql.connector
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("JWT_SECRET", "")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "jowarai_db"),
    )


def create_access_token(user_id: int, role: str) -> str:
    if not SECRET_KEY or SECRET_KEY == "replace_this_with_a_long_random_secret":
        raise RuntimeError("Configure a secure JWT_SECRET in your .env file.")

    expires = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expires,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


def validate_password(password: str):
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one letter and one number.",
        )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if not SECRET_KEY:
            raise credentials_error

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise credentials_error

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, name, email, role FROM users WHERE id = %s",
            (user_id,),
        )
        user = cursor.fetchone()

        if not user:
            raise credentials_error

        return user

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def require_admin(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return current_user


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    validate_password(data.password)

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # All public registrations receive the user role.
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (%s, %s, %s, 'user')
            """,
            (
                data.name.strip(),
                data.email.lower(),
                password_hash.hash(data.password),
            ),
        )

        connection.commit()

        return {
            "message": "Registration successful. You can now log in."
        }

    except mysql.connector.IntegrityError:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists.",
        )

    except mysql.connector.Error:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Could not save the account. Check the database connection.",
        )

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


@router.post("/login")
def login(data: LoginRequest):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (data.email.lower(),),
        )

        user = cursor.fetchone()

    except mysql.connector.Error:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable. Please try again.",
        )

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    if not user or not password_hash.verify(
        data.password, user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password.",
        )

    token = create_access_token(user["id"], user["role"])

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        },
    }


@router.get("/me")
def get_me(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return current_user


@router.get("/admin")
def admin_dashboard(
    admin: Annotated[dict, Depends(require_admin)]
):
    return {
        "message": "Administrator access verified.",
        "admin": admin,
    }
