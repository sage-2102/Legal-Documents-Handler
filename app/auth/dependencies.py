from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError

from app.core.security import (
    SECRET_KEY,
    ALGORITHM
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        role = payload.get("role")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "email": email,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


async def lawyer_only(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] != "lawyer":
        raise HTTPException(
            status_code=403,
            detail="Only lawyers allowed"
        )

    return current_user


async def client_only(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients allowed"
        )

    return current_user


async def admin_only(
    current_user=Depends(
        get_current_user
    )
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins allowed"
        )

    return current_user