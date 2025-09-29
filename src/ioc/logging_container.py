from dependency_injector import containers, providers

from logger import logger


class LoggingContainer(containers.DeclarativeContainer):
    """Container for the logging module"""

    logger = providers.Object(logger)
