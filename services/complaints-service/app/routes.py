from fastapi import APIRouter, Header
from pydantic import BaseModel
from pycommon.auth_client import verify_or_401, require_admin

router = APIRouter()
COMPLAINTS: list[dict] = []

class ComplaintIn(BaseModel):
    text: str

@router.post("/")
def create(data: ComplaintIn, authorization: str = Header(default="")):
    u = verify_or_401(authorization)
    COMPLAINTS.append({"by": u["sub"], "text": data.text})
    return {"created": True}

@router.get("/")
def list_all(authorization: str = Header(default="")):
    require_admin(authorization)
    return {"items": COMPLAINTS}
