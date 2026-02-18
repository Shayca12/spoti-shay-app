import os

def env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

APP_NAME = env("APP_NAME", "spoti-shay")
ENV = env("ENV", "dev")

JWT_SECRET = env("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = env("JWT_ALG", "HS256")
JWT_EXPIRE_MIN = int(env("JWT_EXPIRE_MIN", "120"))

REQUEST_TIMEOUT = float(env("REQUEST_TIMEOUT", "5"))
AUTH_VERIFY_URL = env("AUTH_VERIFY_URL", "http://auth-service:8000/auth/verify")
