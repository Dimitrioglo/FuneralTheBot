#!/usr/bin/env python
import asyncio
import logging

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from handlers import (
    handle_chance,
    handle_choose,
    handle_phobia,
    handle_to_whom,
    handle_who,
    handle_yang_thug,
    help_command,
    quest_button,
    start,
    start_quest,
)
from ioc.application_container import ApplicationContainer

# Configuration
URL = "https://yourdomain.com"  # <- replace with your actual domain
PORT = 8000
TOKEN = ApplicationContainer.envs().BOT_TOKEN()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Start the bot with webhook instead of polling."""

    # Create application
    application = Application.builder().token(TOKEN).updater(None).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^шанс"), handle_chance))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^выбрать"), handle_choose))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^кто"), handle_who))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^кому"), handle_to_whom))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^фобия"), handle_phobia))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^янг тук"), handle_yang_thug))
    application.add_handler(MessageHandler(filters.Regex(r"(?i)^квест"), start_quest))
    application.add_handler(CallbackQueryHandler(quest_button))

    # Set webhook with Telegram
    await application.bot.set_webhook(url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES)

    # Define Starlette routes
    async def telegram(request: Request) -> Response:
        """Receive Telegram updates and forward them to the bot."""
        await application.update_queue.put(
            Update.de_json(data=await request.json(), bot=application.bot)
        )
        return Response()

    async def health(_: Request) -> PlainTextResponse:
        return PlainTextResponse(content="Bot is running 🚀")

    starlette_app = Starlette(
        routes=[
            Route("/telegram", telegram, methods=["POST"]),
            Route("/healthcheck", health, methods=["GET"]),
        ]
    )

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=starlette_app,
            host="0.0.0.0",
            port=PORT,
            use_colors=False,
        )
    )

    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    container = ApplicationContainer()
    container.init_resources()
    container.wire(modules=[__name__])

    asyncio.run(main())
