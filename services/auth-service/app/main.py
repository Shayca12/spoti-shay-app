import os
from fastapi import FastAPI
from pycommon.metrics import metrics_response, metrics_middleware
from pycommon.security import hash_password
from .routes import router, USERS

SERVICE = "auth-service"
app = FastAPI(title=SERVICE)

@app.on_event("startup")
def seed_admin():
    # יוצר משתמש אדמין אוטומטית אם הגדרת משתני סביבה
    email = os.getenv("ADMIN_EMAIL", "admin@spoti-shay.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin123!")
    if email not in USERS:
        USERS[email] = {"password_hash": hash_password(password), "role": "admin"}

@app.middleware("http")
async def _m(request, call_next):
    return await metrics_middleware(request, call_next, SERVICE)

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": SERVICE}

@app.get("/metrics")
def metrics():
    return metrics_response()

app.include_router(router, prefix="/auth")
