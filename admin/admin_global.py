from admin.models.user_admin import *
from admin.models.contract_admin import *
from admin.models.chat_admin import *
from typing import Union
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from admin_setup import google


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Union[bool, RedirectResponse]:
        user = request.session.get('user')

        if not user:
            redirect_uri = request.url_for('login_google')
            return await google.authorize_redirect(request, redirect_uri)

        return True


admin_models = [RoleAdmin, UserAdmin, SpecificationAdmin, ContractAdmin, AgreementAdmin,
                ChatAdmin]