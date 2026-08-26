from fastapi import APIRouter, Depends
from pydantic import BaseModel
from supabase_auth.errors import AuthApiError
from fastapi.responses import JSONResponse, Response

from dependencies import get_current_user
from supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/signup", status_code=201)
def signup(body: AuthRequest):
    email = (body.email or "").strip()
    password = body.password or ""
    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"},
        )
    try:
        resp = supabase.auth.sign_up({"email": email, "password": password})
    except AuthApiError as e:
        return JSONResponse(status_code=400, content={"error": e.message})
    assert resp.user is not None
    return {
        "user": {
            "id": resp.user.id,
            "email": resp.user.email,
            "created_at": resp.user.created_at,
        }
    }


@router.post("/login")
def login(body: AuthRequest):
    email = (body.email or "").strip()
    password = body.password or ""
    if not email or not password:
        return JSONResponse(
            status_code=400,
            content={"error": "Email and password are required"},
        )
    try:
        resp = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    except AuthApiError:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid login credentials"},
        )
    assert resp.session is not None
    return {
        "access_token": resp.session.access_token,
        "refresh_token": resp.session.refresh_token,
    }


@router.post("/logout", status_code=204)
def logout(user: dict = Depends(get_current_user)):
    supabase.auth.sign_out()
    return Response(status_code=204)
