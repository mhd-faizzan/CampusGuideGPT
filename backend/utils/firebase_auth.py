import os
import json
import firebase_admin
from firebase_admin import credentials, auth as fb_auth
from fastapi import Request, HTTPException

_cred_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
if _cred_json:
    cred = credentials.Certificate(json.loads(_cred_json))
    firebase_admin.initialize_app(cred)


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