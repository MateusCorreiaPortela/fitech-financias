from fastapi import APIRouter
from src.app.auth.controller import router as auth_router
from src.app.user.controller import router as user_router
from src.app.category.controller import router as category_router
from src.app.transaction.controller import router as transaction_router
from src.app.report.controller import router as report_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(category_router)
router.include_router(transaction_router)
router.include_router(report_router)
