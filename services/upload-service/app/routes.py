import uuid
from fastapi import APIRouter, Header, UploadFile, File, HTTPException
from pycommon.auth_client import verify_or_401

router = APIRouter()

# "Storage" זמני בזיכרון (אחר כך MinIO)
SONGS_BYTES: dict[str, bytes] = {}     # song_id -> bytes
SONGS_META: dict[str, dict] = {}      # song_id -> meta

@router.post("/song")
async def upload_song(
    authorization: str = Header(default=""),
    file: UploadFile = File(...)
):
    u = verify_or_401(authorization)

    if not file.filename:
        raise HTTPException(400, "missing_filename")

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(400, "empty_file")

    song_id = str(uuid.uuid4())
    SONGS_BYTES[song_id] = data
    SONGS_META[song_id] = {
        "id": song_id,
        "filename": file.filename,
        "content_type": file.content_type or "application/octet-stream",
        "size": len(data),
        "owner": u["sub"],
    }
    return {"uploaded": True, "song": SONGS_META[song_id]}

@router.get("/songs")
def list_my_songs(authorization: str = Header(default="")):
    u = verify_or_401(authorization)
    items = [m for m in SONGS_META.values() if m["owner"] == u["sub"]]
    return {"items": items}

def _export_catalog():
    # מיועד ל-admin/stream לקבל מטא-דאטה “בקלות” בשלב הזה
    return {"meta": SONGS_META, "bytes": SONGS_BYTES}

@router.get("/_debug/catalog")
def debug_catalog():
    # לא לחשוף בפרוד! רק לדמו.
    return {"count": len(SONGS_META)}
