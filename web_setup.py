import asyncio
import uvloop

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from admin.admin_global import google, AdminAuth, admin_models
from settings import config_parameters, is_prod
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.database import engine
from api.router_global import router


def create_app() -> FastAPI:
    docs_url = '/docs' if not config_parameters.IS_PROD else None
    redoc_url = '/redoc' if not config_parameters.IS_PROD else None
    app = FastAPI(title='Shedevro.API', debug=not config_parameters.IS_PROD,
                  docs_url=docs_url, redoc_url=redoc_url,
                  root_path='/api')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    app.add_middleware(SessionMiddleware, secret_key=config_parameters.SECRET_KEY)
    app.mount('/static', StaticFiles(directory=config_parameters.STATIC_DIR), name='static')

    return app

uvloop.install()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
server = create_app()

server.include_router(router)

admin = Admin(app=server, engine=engine, authentication_backend=AdminAuth(config_parameters.SECRET_KEY))

if is_prod:
    print('PROD')


@server.on_event('startup')
async def on_startup_():
    for model in admin_models:
        admin.add_view(model)


@admin.app.route('/auth/google')
async def login_google(request: Request) -> RedirectResponse:
    token = await google.authorize_access_token(request)
    user = token.get('userinfo')

    if user['email'] in config_parameters.OAUTH_CLIENT_EMAILS.split(','):
        request.session['user'] = user

    return RedirectResponse(request.url_for("admin:index"))
