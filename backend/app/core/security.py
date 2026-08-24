from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plaintext password using the configured password hasher."""
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored password hash."""
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Create a signed JWT access token containing the user's ID."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> int:
    """Decode a JWT and return its authenticated user ID."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

    except jwt.PyJWTError as exc:
        # Convert all JWT errors, including expired tokens,
        # into ValueError so the authentication dependency
        # can return HTTP 401 instead of HTTP 500.
        raise ValueError("Invalid or expired access token") from exc

    user_id = payload.get("sub")

    if user_id is None:
        raise ValueError("Token does not contain a user ID")

    try:
        return int(user_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid user ID in access token") from exc
