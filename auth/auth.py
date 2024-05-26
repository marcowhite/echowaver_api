from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from config import SECRET

cookie_transport = CookieTransport(cookie_name="Echowaver", cookie_max_age=360000)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=360000)


auth_backend = AuthenticationBackend(name="jwt",transport=cookie_transport,get_strategy=get_jwt_strategy,)
