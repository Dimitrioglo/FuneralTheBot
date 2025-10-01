import os

from dependency_injector import containers, providers
from dotenv import load_dotenv

load_dotenv()


class SettingsContainer(containers.DeclarativeContainer):
    API_ID = providers.Object(os.getenv("API_ID", ""))
    API_HASH = providers.Object(os.getenv("API_HASH", ""))
    BOT_TOKEN = providers.Object(os.getenv("BOT_TOKEN", ""))
    GIPHY_TOKEN = providers.Object(os.getenv("GIPHY_TOKEN", ""))
