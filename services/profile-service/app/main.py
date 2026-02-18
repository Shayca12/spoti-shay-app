from fastapi import FastAPI
from pycommon.metrics import metrics_response, metrics_middleware
from .routes import router

SERVICE = "profile-service"
app = FastAPI(title=SERVICE)

@app.middleware("http")
async def _m(request, call_next):
    return await metrics_middleware(request, call_next, SERVICE)

@app.get("/healthz")
def healthz():
    return {"ok": True, "service": SERVICE}

@app.get("/metrics")
def metrics():
    return metrics_response()

app.include_router(router, prefix="/profile")
