import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, auth as fb_auth
from fastapi import Request, HTTPException

logger = logging.getLogger(__name__)

_KEY_FILE = os.path.join(os.path.dirname(__file__), os.pardir, "firebase-key.json")


def _init_firebase():
    if firebase_admin._apps:
        return

    cred_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if cred_json:
        cred = credentials.Certificate(json.loads(cred_json))
    elif os.path.exists(_KEY_FILE):
        cred = credentials.Certificate(_KEY_FILE)
    else:
        logger.warning(
            "no firebase credentials — set FIREBASE_SERVICE_ACCOUNT or add backend/firebase-key.json"
        )
        return

    try:
        firebase_admin.initialize_app(cred)
    except ValueError:
        pass  # already initialized (uvicorn --reload re-import)


_init_firebase()


def verify_token(request: Request):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing or invalid auth header")

    token = header.split("Bearer ")[1]
    try:
        decoded = fb_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    if not decoded.get("email_verified", False):
        raise HTTPException(status_code=403, detail="email not verified")

    return decoded
