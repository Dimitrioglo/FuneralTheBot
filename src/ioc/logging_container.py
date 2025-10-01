import logging
from dependency_injector import containers, providers


class LoggingContainer(containers.DeclarativeContainer):
    """Container for the logging module"""

    logger = providers.Singleton(
        logging.getLogger,
        "bot",
    )
