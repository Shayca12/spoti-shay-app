from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pycommon.auth_client import verify_or_401

router = APIRouter()

# NOTE: כרגע אין לנו MinIO/DB, אז אין “shared storage” בין pods.
# בשלב ה-platform נחליף ל-MinIO ואז stream יהיה אמיתי מה-storage.
# כדי שיהיה “דמו עובד” לוקאלית: נשים catalog פנימי (ריק) + הודעה ברורה.

@router.get("/song/{song_id}")
def stream_song(song_id: str, authorization: str = Header(default="")):
    verify_or_401(authorization)
    raise HTTPException(
        501,
        "stream_not_implemented_until_platform_minio (we will connect this in platform repo)"
    )
