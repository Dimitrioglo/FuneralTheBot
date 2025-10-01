from typing import Any

from async_lru import alru_cache
from telethon import TelegramClient

from ioc.application_container import ApplicationContainer
from ioc.logging_container import LoggingContainer

logger = LoggingContainer.logger()


@alru_cache(maxsize=20)
async def get_all_participants(chat_id: int) -> list[dict[str, Any]]:
    participants_list = []
    async with TelegramClient(
        "session",
        ApplicationContainer.envs().API_ID(),
        ApplicationContainer.envs().API_HASH(),
    ) as client:
        async for user in client.iter_participants(chat_id):
            participants_list.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.first_name,
                    # + (" " + user.last_name if user.last_name else ""),
                }
            )
    logger.info(f"Chats fetched: {participants_list}")
    return participants_list
