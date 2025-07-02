from abc import ABCMeta, abstractmethod

from user.domain.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        # find by email, if there is no email, raise HTTPEception 422
        raise NotImplementedError