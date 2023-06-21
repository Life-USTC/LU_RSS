import base64
from requests import Request

from .authenticator import Authenticator


class BasicAuthenticator(Authenticator):
    """The BasicAuthenticator is used to add basic authentication information to requests.

    Basic Authorization will be sent as an Authorization header in the form:

        Authorization: Basic <encoded username and password>

    Args:
        username: User-supplied username for basic auth.
        password: User-supplied password for basic auth.

    Raises:
        ValueError: The username or password is not specified or contains invalid characters.
    """

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.validate()
        self.authorization_header = self.__construct_basic_auth_header()

    def validate(self) -> None:
        """Validate username and password.

        Ensure the username and password are valid for service operations.

        Raises:
            ValueError: The username and/or password is not valid for service operations.
        """
        if self.username is None or self.password is None:
            raise ValueError('The username and password shouldn\'t be None.')

    def __construct_basic_auth_header(self) -> str:
        auth_str = "{0}:{1}".format(self.username, self.password)
        base64_authorization = base64.b64encode(
            auth_str.encode('utf-8')).decode('utf-8')
        return 'Basic {0}'.format(base64_authorization)

    def authenticate(self, req: Request) -> None:
        """Add basic authentication information to a request.

        Basic Authorization will be added to the request's headers in the form:

            Authorization: Basic <encoded username and password>

        Args:
            req: The request to add basic auth information too. Must contain a key to a dictionary
            called headers.
        """
        headers = req.get('headers')
        headers['Authorization'] = self.authorization_header
