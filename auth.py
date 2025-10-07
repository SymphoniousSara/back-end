import os
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="Symphony_Birthday_App",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url=os.getenv("AUTHORIZE_URL"),
    authorize_params=None,
    access_token_url=os.getenv("ACCESS_TOKEN_URL"),
    access_token_method=None,
    refresh_token_method=None,
    authorize_stat=os.getenv("SECRET_KEY"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    jwks_uri=os.getenv("JWKS_URI"),
    client_kwargs={"scope": "openid profile email"},
)