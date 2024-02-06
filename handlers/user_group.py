from string import punctuation
from datetime import datetime, timedelta

from aiogram import F, Bot, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from sqlalchemy import and_


from kbds.reply import get_keyboard
from common.restricted_words import restricted_words
# from filters.chat_types import ChatTypeFilter
from database.db import User, Post, session



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


@user_group_router.message(F.text.lower() == "питання реклами")
@user_group_router.message(Command("ad"))
async def ad_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Підвищення ліміту розміщення оголошень в день:"),
            "До 10 оголошень (включно) - 50 грн.;",
            "Безлім - 100 грн.;",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("До платних оголошень відносяться:"),
            "Будь-які сигарети, вейпи, кальяни, тютюн, glo/iqos...;",
            "Алкоголь;",
            "Медичні товари, БАДи та ін.;",
            "Пости з посиланнями на Ваші ресурси;",
            'Операції з комерційною нерухомістю',
            "Продаж первинної нерухомості від забудовника",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Публікація платних оголошень:"),
            "на дошці Вашого міста - 100 грн./оголошення;",
            "на дошках 3 міст (на вибір) - 250 грн./оголошення;",
            "на дошках 5 міст (на вибір) - 300 грн./оголошення;",
            "на дошках 10 міст (на вибір) - 500 грн./оголошення;",
            'на дошках усіх міст платформи "Місцеві оголошення" - 1000 грн./оголошення',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Розміщення одного оголошення в закріпленнях:"),
            "на дошці Вашого міста - 100 грн./оголошення;",
            "на дошках 3 міст (на вибір) - 250 грн./оголошення;",
            "на дошках 5 міст (на вибір) - 300 грн./оголошення;",
            "на дошках 10 міст (на вибір) - 500 грн./оголошення;",
            'на дошках усіх міст платформи "Місцеві оголошення" - 1000 грн./оголошення',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Автоматичний репост оголошення:"),
            "Публікація 7 днів - 70 грн.;",
            "Публікація 30 днів - 280 грн.;",
            marker="✅ ",
        ),
        sep="\n----------------------\n",
    )
    await message.answer(text="По питаннях реклами звертатися до @trueaaabot")
    await message.answer(text.as_html())



@user_group_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):

    await bot.send_message(
        chat_id=message.chat.id, 
        text=f'''Вітаємо Вас, {message.from_user.first_name}!
    Ви вступили до групи, в якій можна купити чи продати все, що Вам необхідно.
    Ознайомтеся із правилами групи.
    Дякую за розуміння!''',
        reply_markup=get_keyboard(
            "Правила групи",
            "Питання реклами",
            placeholder="Розмістіть оголошення або оберіть розділ:",
            sizes=(2,)
        ),
    )


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    text = ''
    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    else:
        text = "медіа"

    if restricted_words.intersection(clean_text(text.lower()).split()):
        await message.answer(
            f"{message.from_user.full_name}, Вас забанено! Образи та нецензурна лайка заборонені правилами групи!"
            )
        await message.delete()
        # await message.chat.ban(message.from_user.id)
    else:
        user = session.query(User).filter_by(user_id=message.from_user.id).first()
        if not user:
            user = User(user_id=message.from_user.id, full_name=message.from_user.full_name,)
            session.add(user)
            session.commit()
        else:
            posts = session.query(Post).filter(
                    Post.user_id==message.from_user.id, 
                    (datetime.now() - timedelta(days=1)) < Post.created_at,
                    Post.created_at < datetime.now()
                    ).all()
            if len(posts) >= 3:
                await message.delete()
                text = f"{message.from_user.first_name}, Ви перевищили ліміт повідомлень за останні 24 години!"
                await message.answer(text=text)
            else:
                post = Post(
                    post_id=message.message_id,
                    user_id=message.from_user.id,
                    text=text,
                    city=message.chat.username.split("_")[0]
                )
                session.add(post)
                session.commit()

    

