from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from ioc.services_container import ServicesContainer
from exceptions.validation_error import ValidationError
from exceptions.giphy_api_erorr import GiphyAPIError, GiphyNotFound


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ServicesContainer.base_commands_service().start(update)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ServicesContainer.base_commands_service().process_help(update)
    

async def handle_chance(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    _, tail = await ServicesContainer.formatter_service().extract_command(
        update
    )
    await ServicesContainer.base_commands_service().chance(update, tail)


async def handle_who(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    _, tail = await ServicesContainer.formatter_service().extract_command(
        update
    )
    await ServicesContainer.base_commands_service().who(update, tail)


async def handle_choose(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    _, tail = await ServicesContainer.formatter_service().extract_command(
        update
    )
    await ServicesContainer.base_commands_service().choose(update, tail)


async def handle_to_whom(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    _, tail = await ServicesContainer.formatter_service().extract_command(
        update
    )

    await ServicesContainer.base_commands_service().whom(update, tail)


async def handle_giphy(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    _, tail = await ServicesContainer.formatter_service().extract_command(
        update
    )
    await ServicesContainer.base_commands_service().giphy(update, tail)


async def global_error_handler(
    update: object, context: ContextTypes.DEFAULT_TYPE
):
    if isinstance(context.error, ValidationError):
        return

    if isinstance(context.error, GiphyAPIError):
        return

    if isinstance(context.error, GiphyNotFound):
        await update.effective_chat.send_message(f'Гифка по запросу «{update.message.text.strip()}» не найдена')
