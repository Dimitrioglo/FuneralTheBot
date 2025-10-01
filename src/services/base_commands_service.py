import random

from telegram import ForceReply, Update

from services.participants_service import ParticipantsService
from exceptions.validation_error import ValidationError
from ioc.logging_container import LoggingContainer
from services.giphy_service import GiphyService

logger = LoggingContainer.logger()


class BaseCommandsService:
    def __init__(
        self,
        participants_service: ParticipantsService,
        giphy_service: GiphyService,
    ):
        self.participants_service = participants_service
        self.giphy_service = giphy_service

    async def process_help(self, update: Update) -> None:
        help_text = (
            "🤖 <b>Доступные команды:</b>\n\n"
            "🎲 <b>шанс</b> – узнать вероятность чего-то\n"
            "🤹 <b>выбрать</b> – бот поможет выбрать из вариантов\n"
            "🧑‍🤝‍🧑 <b>кто</b> – бот выберет случайного человека\n"
            "🎁 <b>кому</b> – бот определит, кому что-то достанется\n"
            "🎬 <b>гиф</b> – отправить случайный GIF\n"
        )
        await update.effective_chat.send_message(help_text, parse_mode="HTML")

    async def start(self, update: Update) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def chance(self, update: Update, tail: str) -> None:
        percent = random.randint(0, 100)
        reply = f"🔮 Шанс «{tail}» – {percent}%"
        await update.effective_chat.send_message(reply)

    async def who(self, update: Update, tail: str) -> None:
        users_with_username = (
            await self.participants_service.get_all_participants(
                update.effective_chat.id
            )
        )
        random_user = random.choice(users_with_username)
        mention = f"[{random_user.get('full_name')}](tg://user?id={random_user.get('id')})"
        await update.effective_chat.send_message(
            text=f"🔮 {mention} {tail}", parse_mode="Markdown"
        )

    async def choose(self, update: Update, tail: str) -> None:
        options = [opt.strip() for opt in tail.split(",") if opt.strip()]

        if len(options) < 2:
            reply = "Укажи хотя бы два варианта через запятую!"
            await update.effective_chat.send_message(reply)
            raise ValidationError("Validation error")

        choice = random.choice(options)
        reply = f"🔮 Я выбираю «{choice}»"

        await update.effective_chat.send_message(reply)

    async def whom(self, update: Update, tail: str) -> None:
        users_with_username = (
            await self.participants_service.get_all_participants(
                update.effective_chat.id
            )
        )
        random_user = random.choice(users_with_username)
        mention = f"[{random_user.get('full_name')}](tg://user?id={random_user.get('id')})"
        await update.effective_chat.send_message(
            text=f"🔮 Пользователю {mention} {tail}", parse_mode="Markdown"
        )

    async def giphy(self, update: Update, tail: str) -> None:
        gif_url = (
            await self.giphy_service.search_gif(tail)
            if tail
            else await self.giphy_service.fetch_random_gif() 
        )
        await update.effective_chat.send_animation(gif_url)
