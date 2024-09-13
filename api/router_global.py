from fastapi import APIRouter
from api.routes.user_routes import router as user_router
from api.routes.contract_routes import router as contract_router
# from api.routes.chat_routes import router as chat_router


router = APIRouter()

router.include_router(user_router)
router.include_router(contract_router)
# router.include_router(chat_router)