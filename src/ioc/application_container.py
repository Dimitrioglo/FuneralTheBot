from dependency_injector import containers, providers

from ioc.settings_container import SettingsContainer


class ApplicationContainer(containers.DeclarativeContainer):
    envs = providers.Singleton(SettingsContainer)
