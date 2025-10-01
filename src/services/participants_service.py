from typing import Any

from async_lru import alru_cache
from telethon import TelegramClient

from ioc.logging_container import LoggingContainer

logger = LoggingContainer.logger()

class ParticipantsService:
    def __init__(self, api_id: str, api_hash: str):
        self.api_id = api_id
        self.api_hash = api_hash

    @alru_cache(maxsize=20)
    async def get_all_participants(
        self, chat_id: int, with_username: bool = True
    ) -> list[dict[str, Any]]:
        participants_list = []
        try:
            async with TelegramClient(
                "session", self.api_id, self.api_hash
            ) as client:
                async for user in client.iter_participants(chat_id):
                    if with_username and not user.username:
                        continue
                    participants_list.append(
                        {
                            "id": user.id,
                            "username": user.username,
                            "full_name": user.first_name
                            + (" " + user.last_name if user.last_name else ""),
                        }
                    )
            return participants_list
        except Exception as error:
            logger.warning(error)
