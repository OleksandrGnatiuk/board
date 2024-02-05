from string import punctuation

from aiogram import F, Bot, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.utils.formatting import (
    as_list,
    as_marked_section,
    Bold,
)  # Italic, as_numbered_list и тд

from kbds.reply import get_keyboard
from common.restricted_words import restricted_words
# from filters.chat_types import ChatTypeFilter



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



@user_group_router.message(
    (F.text.lower().contains("правила")) | (F.text.lower() == "правила групи"))
@user_group_router.message(Command("rules"))
async def rules_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Дозволено:"),
            "Розміщення товарів без посилань на інші канали та сайти (1 пост = 1 товар);",
            '3 (три) оголошення на день на платформі "Місцеві оголошення";',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Платне розміщення:"),
            "купівля/продаж/оренда комерційної нерухомості;",
            "продаж первинної нерухомісті (від забудовника);",
            "Алкогольні напої;",
            "Тютюнові вироби, вайп;",
            "Медикаменти, бади;",
            marker="💲 ",
        ),
        as_marked_section(
            Bold("Заборонено:"),
            "Розміщення будь-яких посилань;",
            "Образи та нецензурна лайка;",
            "Надто великий текст (понад 500 символів);",
            "Фейкові товари/ послуги/ криминал - бан;",
            "Реклама на фото інших груп;",
            "Мультиаккаунти блокуватимуться;",
            marker="❌ ",
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
            "До 10 оголошень (включно) - 50 грн./доба;",
            "Безлім - 100 грн./доба;",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Публікація КОМЕРЦІЙНИХ оголошень:"),
            "на дошці Вашого міста - 100 грн./оголошення;",
            "на дошках 3 міст (на вибір) - 250 грн./оголошення;",
            "на дошках 5 міст (на вибір) - 300 грн./оголошення;",
            "на дошках 10 міст (на вибір) - 500 грн./оголошення;",
            'на дошках усіх міст платформи "Місцеві оголошення" - 1000 грн./оголошення',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Розміщення приватного оголошення в закріпленнях:"),
            "на дошці Вашого міста - 100 грн./оголошення;",
            "на дошках 3 міст (на вибір) - 250 грн./оголошення;",
            "на дошках 5 міст (на вибір) - 300 грн./оголошення;",
            "на дошках 10 міст (на вибір) - 500 грн./оголошення;",
            'на дошках усіх міст платформи "Місцеві оголошення" - 1000 грн./оголошення',
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Авторепост оголошення:"),
            "Кожні 2 години - 200 грн./доба;",
            "Кожна 1 година - 300 грн./доба;",
            marker="✅ ",
        ),
        sep="\n----------------------\n",
    )
    await message.answer(text.as_html())



@user_group_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):

    await bot.send_message(
        chat_id=message.chat.id, 
        text="Розмістіть оголошення або оберіть розділ",
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
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(
            f"{message.from_user.full_name}, Вас забанено! Образи та нецензурна лайка заборонені правилами групи!"
        )
        await message.delete()
        # await message.chat.ban(message.from_user.id)
