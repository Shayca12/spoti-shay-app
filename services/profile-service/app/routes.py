from fastapi import APIRouter, Header
from pydantic import BaseModel
from pycommon.auth_client import verify_or_401

router = APIRouter()
PROFILES: dict[str, dict] = {}

class ProfileIn(BaseModel):
    display_name: str
    avatar_url: str | None = None

@router.get("/me")
def me(authorization: str = Header(default="")):
    u = verify_or_401(authorization)
    return PROFILES.get(u["sub"], {"display_name": u["sub"], "avatar_url": None})

@router.put("/me")
def update_me(data: ProfileIn, authorization: str = Header(default="")):
    u = verify_or_401(authorization)
    PROFILES[u["sub"]] = data.model_dump()
    return {"updated": True}
