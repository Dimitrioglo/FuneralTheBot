from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from handlers import (
    global_error_handler,
    handle_chance,
    handle_choose,
    handle_giphy,
    handle_to_whom,
    handle_who,
    handle_help,
    start,
)
from ioc.application_container import ApplicationContainer


def app() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    application = (
        Application.builder()
        .token(ApplicationContainer.envs().BOT_TOKEN())
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        MessageHandler(filters.Regex(r"(?i)^шанс"), handle_chance)
    )
    application.add_handler(
        MessageHandler(filters.Regex(r"(?i)^выбрать"), handle_choose)
    )
    application.add_handler(
        MessageHandler(filters.Regex(r"(?i)^кто"), handle_who)
    )
    application.add_handler(
        MessageHandler(filters.Regex(r"(?i)^кому"), handle_to_whom)
    )
    application.add_handler(
        MessageHandler(filters.Regex(r"(?i)^гиф"), handle_giphy)
    )
    application.add_handler(
        MessageHandler(filters.Regex(r"(?i)^помощь"), handle_help)
    )
    application.add_error_handler(global_error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    container = ApplicationContainer()
    container.init_resources()
    container.wire(modules=[__name__])
    app()
