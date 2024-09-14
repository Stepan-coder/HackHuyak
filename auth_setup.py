from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from api.services.auth import *
from models.contract_models import User
from settings import config_parameters


cookie_transport = CookieTransport(cookie_name=config_parameters.AUTH_COOKIE_NAME, cookie_max_age=3600 * 5,
                                   cookie_secure=False, cookie_samesite='none')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config_parameters.AUTH_SECRET, lifetime_seconds=3600,)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

