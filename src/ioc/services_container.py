from dependency_injector import containers, providers

from ioc.application_container import ApplicationContainer
from services.base_commands_service import BaseCommandsService
from services.formatter_service import FormatterService
from services.participants_service import ParticipantsService
from services.validator_service import ValidatorService


class ServicesContainer(containers.DeclarativeContainer):
    validator_service = providers.Singleton(ValidatorService)
    formatter_service = providers.Singleton(FormatterService, validator_service)
    participants_service = providers.Singleton(
        ParticipantsService,
        ApplicationContainer.envs().API_ID(),
        ApplicationContainer.envs().API_HASH(),
    )
    base_commands_service = providers.Singleton(
        BaseCommandsService, participants_service
    )
