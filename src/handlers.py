import random

from telegram import ForceReply, Update
from telegram.ext import (
    ContextTypes,
)

from ioc.services_container import ServicesContainer
from proto.get_chat_members import get_all_participants


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def handle_chance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    command, tail = ServicesContainer.formatter_service().extract_command(update)

    if not tail:
        reply = "Неправильное использование - «шанс [текст]»"
        await update.message.reply_text(reply)
        return

    percent = random.randint(0, 100)

    reply = f"Шанс «{tail}» – {percent}%"
    await update.message.reply_text(reply)


async def handle_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.strip()

    parts = message_text.split(maxsplit=1)
    tail = parts[1] if len(parts) > 1 else ""

    if not tail:
        reply = "Неправильное использование – «Выбрать [вариант 1], [вариант 2], [вариант 3] ...»"
        await update.message.reply_text(reply)
        return

    # Разбиваем строку по запятым
    options = [opt.strip() for opt in tail.split(",") if opt.strip()]

    if len(options) < 2:
        reply = "Укажи хотя бы два варианта через запятую!"
        await update.message.reply_text(reply)
        return

    # Выбираем случайный вариант
    choice = random.choice(options)
    reply = f"Я выбираю «{choice}»"

    await update.message.reply_text(reply)

async def handle_who(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command, tail = ServicesContainer.formatter_service().extract_command(update)

    if not tail:
        reply = "Неправильное использование - кто [текст]»"
        await update.message.reply_text(reply)
        return

    participants = await get_all_participants(update.effective_chat.id)
    users_with_username = [u for u in participants if u["username"]]

    if not users_with_username:
        return None

    random_user = random.choice(users_with_username)["username"]
    await update.message.reply_text(f"@{random_user}, {tail}")


async def handle_to_whom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command, tail = ServicesContainer.formatter_service().extract_command(update)

    if not tail:
        reply = "Неправильное использование - кому [текст]»"
        await update.message.reply_text(reply)
        return

    participants = await get_all_participants(update.effective_chat.id)
    users_with_username = [u for u in participants if u["username"]]

    if not users_with_username:
        return None

    random_user = random.choice(users_with_username)["username"]
    await update.message.reply_text(f"Пользователю @{random_user} {tail}")


async def handle_phobia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    fears = [
        "боится котов в шляпах",
        "ужасается пустых холодильников",
        "панически избегает клоунов с гитарой",
        "не переносит холодный чай",
        "боится потерять носки в стиралке",
        "дрожит при виде говорящих попугаев",
        "в ужасе от будильников по утрам",
        "боится сломать каблук в важный момент",
        "опасается лифтов без кнопки 'стоп'",
        "бежит от роботов-пылесосов",
        "боится опоздать на автобус во сне",
        "не переносит звук скрипящего пенопласта",
        "ужасается зелёных огурцов",
        "боится людей в одинаковых свитерах",
        "панически реагирует на длинные очереди",
        "боится забыть пароль от Wi-Fi",
        "дрожит при виде кота с двумя хвостами",
        "боится чайников, которые не свистят",
        "теряется при виде открытых дверей шкафа ночью",
        "в ужасе от сломанных карандашей",
        "боится мыльных пузырей в темноте",
        "опасается пересоленного супа",
        "боится потерять пульт от телевизора",
        "ужасается людей без носков дома",
        "боится застрять в поворотной двери",
        "панически реагирует на пустые сообщения",
        "боится увидеть таракана в наушниках",
        "дрожит от запаха прокисшего молока",
        "боится встретить двойника в метро",
        "в ужасе от смайлика 🙂 без эмоций",
    ]
    fear = random.choice(fears)

    chat_id = update.effective_chat.id
    participants = await get_all_participants(chat_id)


    random_user = random.choice(participants)
    fear = random.choice(fears)

    mention = f"[{random_user['username']}](tg://user?id={random_user['id']})"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{mention}, {fear} 😱",
        parse_mode="Markdown",
    )


async def handle_yang_thug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command, tail = ServicesContainer.formatter_service().extract_command(update)

    if not tail:
        reply = "Неправильное использование - янг тук»"
        await update.message.reply_text(reply)
        return

    chat_id = update.effective_chat.id
    participants = await get_all_participants(chat_id)
    users_with_username = [u for u in participants if u["username"]]


    random_user = random.choice(users_with_username)

    mention = f"[{random_user['username']}](tg://user?id={random_user['id']})"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{mention}, ты уже послушал новый альбом Янг Тука?",
        parse_mode="Markdown",
    )


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# --- События для квеста с диапазонами ---
events = {
    "налево": [
        {"description": "Вы встретили волка 🐺", "fail_range": (3, 6), "reward_range": (0, 2)},
        {"description": "Нашли ягодную поляну 🍓", "fail_range": (0, 1), "reward_range": (1, 3)},
        {"description": "Ничего интересного, просто лес 🌲", "fail_range": (2, 4), "reward_range": (0, 1)},
        {"description": "Вы наткнулись на старый колодец 💧", "fail_range": (0, 1), "reward_range": (1, 4)},
        {"description": "Сквозь деревья мелькнула тень 🦉", "fail_range": (3, 5), "reward_range": (0, 1)},
    ],
    "направо": [
        {"description": "Вы нашли старый сундук 💰", "fail_range": (0, 1), "reward_range": (2, 5)},
        {"description": "Падение с кочки! 😱", "fail_range": (4, 7), "reward_range": (0, 1)},
        {"description": "Маленький ручей, пора пить воду 💧", "fail_range": (1, 3), "reward_range": (0, 1)},
        {"description": "Вы встретили странного странника 🧙", "fail_range": (0, 1), "reward_range": (1, 4)},
        {"description": "Лесная тропинка пуста 🌿", "fail_range": (2, 5), "reward_range": (0, 1)},
    ]
}

# --- Команда /квест ---
async def start_quest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["health"] = random.randint(8, 12)
    context.user_data["steps"] = 0  # количество пройденных шагов
    keyboard = [
        [
            InlineKeyboardButton("Налево", callback_data="quest|налево"),
            InlineKeyboardButton("Направо", callback_data="quest|направо"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты стоишь на развилке таинственного леса 🌲. "
             "Ветер шепчет о приключениях, а дорога полна неожиданностей. Куда ты пойдёшь? 👣",
        reply_markup=reply_markup
    )

async def quest_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")
    if len(data) != 2 or data[0] != "quest":
        return

    choice = data[1]
    event = random.choice(events.get(choice, []))

    # Увеличиваем шаги
    context.user_data["steps"] = context.user_data.get("steps", 0) + 1

    mention = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})"
    text = f"{mention}, {event['description']}"

    # Рандомизация последствий
    health = context.user_data.get("health", 10)
    fail = random.randint(*event.get("fail_range", (0, 0)))
    reward = random.randint(*event.get("reward_range", (0, 0)))

    if fail > 0 and random.random() < 0.7:
        health -= fail
        text += f"\n❌ Потеряно {fail} здоровья. Текущее здоровье: {health}"
    elif reward > 0:
        text += f"\n🎁 Получено {reward}!"

    context.user_data["health"] = health

    # Проверка состояния
    if health <= 0:
        text += f"\n💀 Вы погибли после {context.user_data['steps']} шагов! Квест завершен."
        # Убираем старую клавиатуру
        try:
            await query.message.edit_reply_markup(reply_markup=None)
        except:
            pass
        # Отправляем финальное сообщение
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=text,
            parse_mode="Markdown"
        )
        return

    # --- Создаём новую клавиатуру как отдельное сообщение ---
    keyboard = [
        [
            InlineKeyboardButton("Налево", callback_data="quest|налево"),
            InlineKeyboardButton("Направо", callback_data="quest|направо"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем результат события
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=text,
        parse_mode="Markdown"
    )

    # Отправляем новую клавиатуру как новое сообщение
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text="Куда пойдёшь дальше?",
        reply_markup=reply_markup
    )