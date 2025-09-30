

from telegram import Update


class FormatterService:

    @staticmethod
    def extract_command(update: Update) -> tuple[str, str]:
        message_text = update.message.text.strip()
        parts = message_text.strip().split(maxsplit=1)
        command = parts[0] if parts else ""
        tail = parts[1] if len(parts) > 1 else ""
        return command, tail