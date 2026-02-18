from fastapi import APIRouter, Header
from pycommon.auth_client import require_admin

router = APIRouter()

@router.get("/me")
def admin_me(authorization: str = Header(default="")):
    u = require_admin(authorization)
    return {"admin": True, "sub": u["sub"]}

@router.get("/note")
def note(authorization: str = Header(default="")):
    require_admin(authorization)
    return {
        "msg": "admin endpoints will become real once we connect Postgres/MinIO in platform repo"
    }
