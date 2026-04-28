from pydantic import BaseModel


class UpdateCategoryDto(BaseModel):
    name: str
