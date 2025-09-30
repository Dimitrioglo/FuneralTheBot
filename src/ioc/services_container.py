from dependency_injector import containers, providers

from services.formatter_service import FormatterService


class ServicesContainer(containers.DeclarativeContainer):
    formatter_service = providers.Singleton(FormatterService)
