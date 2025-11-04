from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, Base, engine
from schemas.recipe import RecipeCreate, RecipeResponse, RecipeUpdate
from crud.recipe import get_recipe, get_recipes, create_recipe, delete_recipe, update_recipe, increment_views


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Книга Рецептов",
    description="API для работы с книгой рецептов",
    version="0.1.0",
    lifespan=lifespan
)


@app.get(
    "/recipes",
    response_model=list[RecipeResponse],
    summary="Показать все рецеты",
    description="Выводит на экран все рецепты"
)
async def read_recipes(session: AsyncSession = Depends(get_session)):
    recipes = await get_recipes(session)
    return recipes


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeResponse,
    summary="Показать рецепт",
    description="Выводит на экран рецепт по id"
)
async def read_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)):
    recipe = await get_recipe(session, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    await increment_views(session, recipe)
    return recipe


@app.post(
    "/recipes",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать рецепт",
    description="Создает новый рецепт в базе данных"
)
async def create_new_recipe(recipe: RecipeCreate, session: AsyncSession = Depends(get_session)):
    new_recipe = await create_recipe(session, recipe)
    return new_recipe


@app.put(
    "/recipes/{recipe_id}",
    response_model=RecipeResponse,
    summary="Обновить рецепт",
    description="Обновляет рецепт в базе данных по id"
)
async def update_existing_recipe(recipe_id: int, recipe: RecipeUpdate, session: AsyncSession = Depends(get_session)):
    update_data = recipe.model_dump(exclude_unset=True)
    update = await update_recipe(session, recipe_id, update_data)
    if not update:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return update


@app.delete(
    "/recipes/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаляет рецепт",
    description="Удаляет рецепт в базе данных по id"
)
async def delete_existing_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_recipe(session, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return
