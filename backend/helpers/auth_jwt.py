import os, time, functools
import jwt
from flask import request, abort
JWT_SECRET = os.getenv("JWT_SECRET", "REPLACE_THIS_SECRET")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "3600"))
def create_token(payload: dict):
    payload = dict(payload)
    payload.setdefault("iat", int(time.time()))
    payload.setdefault("exp", int(time.time()) + JWT_EXP_SECONDS)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    if isinstance(token, bytes): token = token.decode()
    return token
def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
def admin_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization") or ""
        if auth.startswith("Bearer "):
            token = auth.split(" ",1)[1]
            try:
                data = decode_token(token)
            except Exception:
                return abort(401, description="Invalid or expired token")
            if data.get("is_admin"):
                request.admin = data
                return f(*args, **kwargs)
        legacy = request.headers.get("X-Admin-Auth")
        if legacy and legacy == os.getenv("ADMIN_PASSWORD"):
            request.admin = {"username": os.getenv("ADMIN_USERNAME")}
            return f(*args, **kwargs)
        return abort(403, description="Unauthorized admin")
    return wrapper
