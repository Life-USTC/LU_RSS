from .authenticator import Authenticator


class NoAuthAuthenticator(Authenticator):
    """Performs no authentication."""
    authentication_type = 'noAuth'

    def validate(self) -> None:
        pass

    def authenticate(self, req) -> None:
        pass
