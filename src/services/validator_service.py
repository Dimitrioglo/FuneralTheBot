from telegram import Update

from exceptions.validation_error import ValidationError


class ValidatorService:
    @staticmethod
    async def validate_tail(update: Update, tail: str, command: str) -> None:
        if tail:
            return None

        match command.lower():
            case "выбрать":
                reply = "Неправильное использование – «Выбрать [вариант 1], [вариант 2], [вариант 3] ...»"
            case _:
                reply = f"Неправильное использование — {command} [текст]"
        await update.effective_chat.send_message(reply)
        raise ValidationError("Validation error")
