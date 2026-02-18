import requests
from fastapi import HTTPException
from .config import AUTH_VERIFY_URL, REQUEST_TIMEOUT

def verify_or_401(authorization: str) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing_bearer")

    r = requests.post(
        AUTH_VERIFY_URL,
        headers={"Authorization": authorization},
        timeout=REQUEST_TIMEOUT
    )
    if r.status_code != 200:
        raise HTTPException(401, "invalid_token")
    return r.json()

def require_admin(authorization: str) -> dict:
    u = verify_or_401(authorization)
    if u.get("role") != "admin":
        raise HTTPException(403, "admin_only")
    return u
