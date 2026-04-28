from fastapi import APIRouter, Depends, Query
from src.app.core.dependencies import get_current_user
from src.app.core.models import User
from src.app.core.pagination import PaginatedResponse
from src.app.category.dto import CreateCategoryDto, UpdateCategoryDto
from src.app.category.responses import CategoryResponse
from src.app.category.service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])
service = CategoryService()


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(dto: CreateCategoryDto, user: User = Depends(get_current_user)):
    return await service.create(user.id, dto)


@router.get("/", response_model=PaginatedResponse[CategoryResponse])
async def list_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
):
    return await service.find_all_by_user(user.id, page, limit)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, user: User = Depends(get_current_user)):
    return await service.find_by_id(category_id, user.id)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, dto: UpdateCategoryDto, user: User = Depends(get_current_user)):
    return await service.update(category_id, user.id, dto)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, user: User = Depends(get_current_user)):
    await service.delete(category_id, user.id)
