from dependency_injector import containers, providers
from user.infra.repository.user_repo import UserRepository
from user.application.user_service import UserService


from utils.crypto import Crypto


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user"
        ],
    )

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)