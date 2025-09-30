import random

from telegram import ForceReply, Update

from services.participants_service import ParticipantsService
from exceptions.validation_error import ValidationError
from ioc.logging_container import LoggingContainer

logger = LoggingContainer.logger()


class BaseCommandsService:
    def __init__(self, participants_service: ParticipantsService):
        self.participants_service = participants_service

    async def start(update: Update) -> None:
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
            text=f"🔮 {mention}, {tail}", parse_mode="Markdown"
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
