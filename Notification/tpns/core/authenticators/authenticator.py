from abc import ABC, abstractmethod


class Authenticator(ABC):
    """This interface defines the common methods and constants associated with an Authenticator implementation."""

    @abstractmethod
    def authenticate(self, req: dict) -> None:
        """Perform the necessary authentication steps for the specified request.

        Attributes:
            req (dict): Will be modified to contain the appropriate authentication information.

        To be implemented by subclasses.
        """
        pass

    @abstractmethod
    def validate(self) -> None:
        """Validates the current set of configuration information in the Authenticator.

        Raises:
            ValueError: The configuration information is not valid for service operations.

        To be implemented by subclasses.
        """
        pass
