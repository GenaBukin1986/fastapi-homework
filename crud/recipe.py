from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from models.recipe import Recipe
from schemas.recipe import RecipeCreate


async def get_recipes(db: AsyncSession):
    stmt = select(Recipe).order_by(desc(Recipe.views), Recipe.cooking_time)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_recipe(db: AsyncSession, recipe_id: int) -> Recipe | None:
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    return result.scalars().first()


async def increment_views(db: AsyncSession, recipe: Recipe) -> None:
    recipe.views += 1
    await db.commit()


async def create_recipe(db: AsyncSession, recipe: RecipeCreate) -> Recipe:
    db_recipe = Recipe(
        name=recipe.name,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
        views=0
    )

    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe


async def update_recipe(db: AsyncSession, recipe_id: int, recipe_data: dict):
    db_recipe = await get_recipe(db, recipe_id)
    if not db_recipe:
        return None

    allowed_fields = {"name", "cooking_time", "ingredients", "description"}
    for key, value in recipe_data.items():
        if key in allowed_fields:
            setattr(db_recipe, key, value)

    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe


async def delete_recipe(db: AsyncSession, recipe_id: int):
    db_recipe = await get_recipe(db, recipe_id)
    if not db_recipe:
        return False
    await db.delete(db_recipe)
    await db.commit()
    return True
