from fastapi import Header, HTTPException

from supabase_client import supabase


def get_current_user(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer ") or len(authorization.split()) < 2:
        raise HTTPException(status_code=401, detail="Access token required")
    token = authorization.split()[1]
    try:
        resp = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if resp is None or resp.user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = resp.user
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }
