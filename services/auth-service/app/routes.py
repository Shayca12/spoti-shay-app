from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from pycommon.security import hash_password, verify_password, create_token, decode_token

router = APIRouter()

# DB בהמשך: כרגע זיכרון
USERS: dict[str, dict] = {}  # email -> {password_hash, role}

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: RegisterIn):
    if data.email in USERS:
        raise HTTPException(409, "user_exists")
    USERS[data.email] = {"password_hash": hash_password(data.password), "role": "user"}
    return {"created": True}

@router.post("/login")
def login(data: LoginIn):
    u = USERS.get(data.email)
    if not u or not verify_password(data.password, u["password_hash"]):
        raise HTTPException(401, "bad_credentials")
    token = create_token(sub=data.email, role=u["role"])
    return {"access_token": token, "token_type": "bearer"}

@router.post("/verify")
def verify(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing_bearer")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(401, "invalid_token")
    return {"valid": True, "sub": payload["sub"], "role": payload.get("role", "user")}
