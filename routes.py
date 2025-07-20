from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db


app = FastAPI()


# @asynccontextmanager
# async def lifespan():
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.create_all)
#
#     yield
#
#     await session.close()
#     await engine.dispose()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/recipes/", response_model=List[schemas.RecipeOut])
async def get_recipes(session: Session = Depends(get_db)) -> List[models.Recipe]:
    req = await session.execute(select(models.Recipe))
    result = req.scalars().all()

    if not result:
        raise HTTPException(status_code=404, detail="There are no recipes")

    return result

@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe_by_id(recipe_id: int, session: Session = Depends(get_db)) -> models.Recipe:
    req = await session.execute(select(models.Recipe).where(models.Recipe.id == recipe_id))
    result = req.scalar_one_or_none()
    print(result)
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not founded.")

    result.count_of_view += 1

    return result

@app.post("/recipes/", response_model=schemas.RecipeOut)
async def create_recipe(recipe: schemas.RecipeIn, session: Session = Depends(get_db)) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.model_dump())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
