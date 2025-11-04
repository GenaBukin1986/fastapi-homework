from typing import Dict

from pydantic import BaseModel, ConfigDict, Field


class RecipeCreate(BaseModel):
    name: str = Field(..., description="Название рецепта", examples=["Омлет", "Борщ"])
    cooking_time: int = Field(
        ..., description="Время приготовления в минутах", ge=1, examples=[10, 45]
    )
    ingredients: Dict[str, float] = Field(
        ...,
        description="Словарь ингредиентов: ключ — название, значение — количество",
        examples=[{"яйцо": 2, "молоко": 100, "соль": 1}],
    )
    description: str = Field(
        ...,
        description="Полное текстовое описание рецепта",
        examples=["Взбейте яйца с молоком, добавьте соль и жарьте на сковороде."],
    )


class RecipeResponse(RecipeCreate):
    id: int = Field(
        ..., description="Уникальный идентификатор рецепта", examples=[1, 42]
    )
    views: int = Field(
        ..., description="Количество просмотров рецепта", examples=[0, 150]
    )

    model_config = ConfigDict(from_attributes=True)


class RecipeUpdate(BaseModel):
    name: str | None = Field(
        None, description="Новое название рецепта", examples=["Французский омлет"]
    )
    cooking_time: int | None = Field(
        None, description="Новое время приготовления в минутах", ge=1, examples=[12]
    )
    ingredients: Dict[str, float] | None = Field(
        None,
        description="Обновлённый список ингредиентов",
        examples=[{"яйцо": 3, "сливки": 50}],
    )
    description: str | None = Field(
        None,
        description="Обновлённое описание",
        examples=["Добавьте сливки для нежности."],
    )
