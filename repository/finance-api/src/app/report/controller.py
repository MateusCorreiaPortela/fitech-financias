from fastapi import APIRouter, Depends
from src.app.core.dependencies import get_current_user
from src.app.core.models import User
from src.app.report.responses import ExpenseByCategoryItem, IncomeVsExpenseItem
from src.app.transaction.responses import SummaryResponse
from src.app.report.service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])
service = ReportService()


@router.get("/summary", response_model=SummaryResponse)
async def summary(user: User = Depends(get_current_user)):
    return await service.summary(user.id)


@router.get("/expense-by-category", response_model=list[ExpenseByCategoryItem])
async def expense_by_category(user: User = Depends(get_current_user)):
    return await service.expense_by_category(user.id)


@router.get("/income-vs-expense", response_model=list[IncomeVsExpenseItem])
async def income_vs_expense(user: User = Depends(get_current_user)):
    return await service.income_vs_expense(user.id)
