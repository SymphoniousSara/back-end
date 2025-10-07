from datetime import timedelta
import os
from fastapi import HTTPException, APIRouter, Request
from starlette.responses import RedirectResponse
from services.auth import create_access_token
from auth import oauth

router = APIRouter()

@router.get("/login")
async def login(req: Request):
    req.session.clear()
    referer = req.headers.get("referer")
    frontend_url = os.getenv("FRONTEND_URL")
    redirect_url = os.getenv("REDIRECT_URL")
    req.session["login_redirect"] = frontend_url

    return await oauth.Symphony_Birthday_App.authorize_redirect(req, redirect_url, prompt='consent')

@router.get("/auth")
async def auth(req: Request):
    try:
        token = await oauth.Symphony_Birthday_App.authorize_access_token(req)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Google Authentication Failed") from e

    try:
        user_info_endpoint = os.getenv("USER_INFO_ENDPOINT")
        headers = {"Authorization": f'Bearer {token["access_token"]}'}
        google_response = req.get(user_info_endpoint, headers=headers)
        user_info = google_response.json()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Google Authentication Failed") from e

    user = token.get("userinfo")
    if user is None:
        raise HTTPException(status_code=401, detail="Google Authentication Failed")

    expires_in = token.get("expires_in")
    user_id = user.get("sub")
    iss = user.get("iss")
    user_email = user.get("email")

    # first_logged_in = datetime.datetime.now(datetime.UTC)
    # last_accessed = datetime.datetime.now(datetime.UTC)

    # current_user_name = user_info.get("name")
    # current_user_picture = user_info.get("picture")

    if iss not in ["https://accounts.google.com", "accounts.google.com"]:
        raise HTTPException(status_code=401, detail="Google Authentication Failed")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Google Authentication Failed")

    # Creating a JWT Token
    access_token_expires = timedelta(seconds=expires_in)
    access_token = create_access_token(
        data={"sub": user_id, "email": user_email},
        expires_delta=access_token_expires
    )

    # For this function we need a utility log function, can be implemented if need be
    #session_id = str(uuid.uuid4())
    # log_user(user_id, user_email, current_user_name, current_user_picture, first_logged_in, last_accessed)
    # log_token(access_token, user_email, session_id)

    redirect_url = req.sesson.pop('login_redirect', '')
    response = RedirectResponse(redirect_url)
    response.set_cookie(
        key = "access_token",
        value = access_token,
        httponly = True,
        secure = True,
        samesite = "strict",
    )

    return response