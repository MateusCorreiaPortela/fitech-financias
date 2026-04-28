from datetime import date
from fastapi import APIRouter, Depends, Query
from src.app.core.dependencies import get_current_user
from src.app.core.models import User
from src.app.core.pagination import PaginatedResponse
from src.app.transaction.dto import CreateTransactionDto, UpdateTransactionDto, TransactionFilterDto, TransactionType
from src.app.transaction.responses import TransactionResponse, BalanceResponse, SummaryResponse
from src.app.transaction.service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])
service = TransactionService()


@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(dto: CreateTransactionDto, user: User = Depends(get_current_user)):
    return await service.create(user.id, dto)


@router.get("/", response_model=PaginatedResponse[TransactionResponse])
async def list_transactions(
    type: TransactionType | None = None,
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    order_by: str = Query("-date"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
):
    filters = TransactionFilterDto(type=type, date_from=date_from, date_to=date_to, order_by=order_by)
    return await service.find_all(user.id, filters, page, limit)


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(user: User = Depends(get_current_user)):
    return await service.get_balance(user.id)


@router.get("/summary", response_model=SummaryResponse)
async def get_summary(user: User = Depends(get_current_user)):
    return await service.get_summary(user.id)


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, user: User = Depends(get_current_user)):
    return await service.find_by_id(transaction_id, user.id)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(transaction_id: int, dto: UpdateTransactionDto, user: User = Depends(get_current_user)):
    return await service.update(transaction_id, user.id, dto)


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: int, user: User = Depends(get_current_user)):
    await service.delete(transaction_id, user.id)
