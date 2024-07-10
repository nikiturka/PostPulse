from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_async_session
from .models import User
from .schemas import UserCreate, UserUpdate

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.get("/")
async def read_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    res = await session.execute(query)
    users = res.scalars().all()

    return users


@users_router.post("/")
async def create_new_user(user_to_create: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query_exists = select(User).where(User.email == user_to_create.email)
    result = await session.execute(query_exists)
    user_exists = result.scalars().first()

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    stmt = insert(User).values(**user_to_create.dict())
    await session.execute(stmt)
    await session.commit()

    return {"response": 200}


@users_router.get("/{user_id}")
async def read_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    res = await session.execute(query)
    user = res.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@users_router.patch("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    existing_user = await session.execute(query)
    user = existing_user.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)
    if update_data:
        update_stmt = update(User).where(User.id == user_id).values(**update_data)
        await session.execute(update_stmt)
        await session.commit()

    return {"message": "User updated successfully"}


@users_router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    existing_user = await session.execute(query)
    user = existing_user.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    delete_stmt = delete(User).where(User.id == user_id)
    await session.execute(delete_stmt)
    await session.commit()

    return {"message": "User deleted successfully"}
