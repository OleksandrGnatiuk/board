from string import punctuation
from datetime import datetime, timedelta

from aiogram import F, Bot, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, session

from kbds.reply import get_keyboard
from common.restricted_words import restricted_words
# from filters.chat_types import ChatTypeFilter
from database.models import User, Post
from database.orm_query import (create_post, create_user, 
                                calc_daily_posts, 
                                get_user, get_post_by_message_id,
                                reduce_num_paid_post, change_post)


user_group_router = Router()
# user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
# user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    #просмотреть все данные и свойства полученных объектов
    #print(admins_list)
    # Код ниже это генератор списка, как и этот x = [i for i in range(10)]
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()
    #print(admins_list)


@user_group_router.message(F.text.lower() == "правила групи")
@user_group_router.message(Command("rules"))
async def rules_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Дозволено:"),
            "Розміщення товарів без посилань на інші канали та сайти (1 пост = 1 товар);",
            'Для полегшення пошуку Ваших оголошень рекомендовано використовувати хештеги, наприклад: #фотоапарат',
            '3 (три) оголошення на день на платформі "Місцеві оголошення";',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Платне розміщення:"),
            "Розміщення понад 3 оголошень в день",
            "купівля/продаж/оренда комерційної нерухомості;",
            "продаж первинної нерухомісті (від забудовника);",
            "Алкогольні напої;",
            "Будь-які сигарети, вейпи, кальяни, тютюн, glo/iqos...",
            "Медичні товари, БАДи та ін.;",
            marker="💲 ",
        ),
        as_marked_section(
            Bold("Заборонено:"),
            "Розміщення будь-яких посилань;",
            "Реклама на фото інших груп;",
            "Надто великий текст (понад 500 символів);",
            "Образи та нецензурна лайка - бан;",
            "Фейкові товари/ послуги/ криминал - бан;",
            marker="🚫 ",
        ),
        sep="\n----------------------\n",
    )
    await message.answer(text.as_html())


@user_group_router.message(F.text.lower() == "питання з реклами")
@user_group_router.message(Command("ad"))
async def ad_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Підвищення ліміту розміщення оголошень в день:"),
            "До 10 оголошень (включно) - 20 грн.;",
            "До 50 оголошень (включно) - 50 грн.;",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("До платних оголошень відносяться:"),
            "Будь-які сигарети, вейпи, кальяни, тютюн, glo/iqos...;",
            "Алкогольні напої;",
            "Медичні товари, БАДи та ін.;",
            "Пости з посиланнями на Ваші ресурси;",
            'Операції з комерційною нерухомістю',
            "Продаж первинної нерухомості від забудовника",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Публікація платних оголошень:"),
            "на дошці Вашого міста - 50 грн./оголошення;",
            "на дошках 3 міст (на вибір) - 120 грн./оголошення;",
            "на дошках 5 міст (на вибір) - 150 грн./оголошення;",
            "на дошках 10 міст (на вибір) - 200 грн./оголошення;",
            'на дошках усіх міст платформи "Місцеві оголошення" - 500 грн./оголошення',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Розміщення одного оголошення в закріпленнях:"),
            "на дошці Вашого міста - 50 грн./оголошення;",
            "на дошках 3 міст (на вибір) - 120 грн./оголошення;",
            "на дошках 5 міст (на вибір) - 150 грн./оголошення;",
            "на дошках 10 міст (на вибір) - 200 грн./оголошення;",
            'на дошках усіх міст платформи "Місцеві оголошення" - 500 грн./оголошення',
            marker="✅ ",
        ),
        sep="\n----------------------\n",
    )
    await message.answer(text="По питаннях реклами звертатися до @trueaaabot")
    await message.answer(text.as_html())
    await message.answer(text="По питаннях реклами звертатися до @trueaaabot")


@user_group_router.message(F.text.lower() == "інші міста")
@user_group_router.message(Command("cities"))
async def cities_cmd(message: types.Message):
    text = """
    Славута-@slavuta_dd | Нетішин-@netishyn_dd |
Шепетівка-@shepetivka_dd | """
    await message.answer(text)


@user_group_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text='...',
        parse_mode=ParseMode.HTML,
        reply_markup=get_keyboard(
            "Правила групи",
            "Інші міста",
            "Питання з реклами",
            placeholder="Розмістіть оголошення або оберіть розділ:",
            sizes=(3,)
        ),
    )


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message, session: AsyncSession):
    text = ''
    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption

    if restricted_words.intersection(clean_text(text.lower()).split()):
        await message.answer(
            f"{message.from_user.full_name}, Вас забанено! Образи та нецензурна лайка заборонені правилами групи!"
            )
        await message.delete()
        # await message.chat.ban(message.from_user.id)
    else:
        user = await get_user(message, session)
        if not user:
            await create_user(message, session)
        
        posts = await calc_daily_posts(message, session)

        if len(posts) >= 3 and int(user.num_paid_post) == 0:
            post = await get_post_by_message_id(message, session)
            if post:
                await change_post(message, session)
            else:
                await message.delete()
                text = f"{message.from_user.first_name}, Ви перевищили ліміт повідомлень за останні 24 години!"
                await message.answer(text=text)
        else:
            await create_post(message, session)
            await reduce_num_paid_post(message, session)
            