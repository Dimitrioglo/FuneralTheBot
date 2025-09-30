from telegram import Update

from services.validator_service import ValidatorService


class FormatterService:
    def __init__(self, validator_service: ValidatorService):
        self.validator_service = validator_service

    async def extract_command(self, update: Update) -> tuple[str, str]:
        message_text = update.message.text.strip()
        parts = message_text.strip().split(maxsplit=1)
        command = parts[0] if parts else ""
        tail = parts[1] if len(parts) > 1 else ""
        await self.validator_service.validate_tail(update, tail, command)
        return command, tail
