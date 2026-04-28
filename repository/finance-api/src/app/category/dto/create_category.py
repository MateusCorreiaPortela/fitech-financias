from pydantic import BaseModel


class CreateCategoryDto(BaseModel):
    name: str
