from datetime import datetime, timedelta
from aiogram import types
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Post


async def get_user(message: types.Message, session: AsyncSession):
    result = await session.execute(select(User).filter_by(user_id=message.from_user.id))
    user = result.scalar()
    return user


async def create_user(message: types.Message, session: AsyncSession):
    user = User(user_id=message.from_user.id, full_name=message.from_user.full_name,)
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def calc_daily_posts(message: types.Message, session: AsyncSession):    
    result = await session.execute(select(Post).filter(
                Post.user_id == message.from_user.id,
                (datetime.now() - timedelta(days=1)) < Post.created_at,
                Post.created_at < datetime.now()
                ))
    posts = result.scalars().all()
    return posts


async def get_post_by_message_id(message: types.Message, session: AsyncSession):
    result = await session.execute(select(Post).filter_by(post_id=message.message_id))
    post = result.scalar()
    return post


async def create_post(message: types.Message, session: AsyncSession):
    post = Post(
          post_id=message.message_id,
          user_id=message.from_user.id,
          text=message.text,
          caption=message.caption,
          city=message.chat.username.split("_")[0]
          )
    session.add(post)
    await session.commit()
    await session.refresh(post)

    
async def reduce_num_paid_post(message: types.Message, session: AsyncSession):
    user = await get_user(message, session)
    if int(user.num_paid_post) > 0:
        user.num_paid_post = int(user.num_paid_post) - 1
        await session.commit()
        await session.refresh(user)


async def change_post(message: types.Message, session: AsyncSession):
    post = await get_post_by_message_id(message, session)
    post.text = message.text
    post.caption = message.caption
    await session.commit()
    await session.refresh(post)
    
