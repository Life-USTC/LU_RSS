from http import HTTPStatus
from requests import Response


class ApiException(Exception):
    """Custom exception class for errors returned from operations.

    Args:
        code: HTTP status code of the error response.
        message: The error response body. Defaults to None.
        http_response: The HTTP response of the failed request. Defaults to None.

    Attributes:
        code (int): HTTP status code of the error response.
        message (str): The error response body.
        http_response (requests.Response): The HTTP response of the failed request.
    """

    def __init__(self, code: int, message: str = None, http_response: Response = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_response = http_response
        if http_response is not None:
            self.message = self.message if self.message else self._get_error_message(
                http_response)

    def __str__(self) -> str:
        msg = 'Error: ' + str(self.message) + ', Code: ' + str(self.code)
        return msg

    @staticmethod
    def _get_error_message(response: Response) -> str:
        error_message = 'Unknown error'
        try:
            error_json = response.json()
            if 'errors' in error_json:
                if isinstance(error_json['errors'], list):
                    err = error_json['errors'][0]
                    error_message = err.get('message')
            elif 'error' in error_json:
                error_message = error_json['error']
            elif 'message' in error_json:
                error_message = error_json['message']
            elif 'errorMessage' in error_json:
                error_message = error_json['errorMessage']
            elif response.status_code == 401:
                error_message = 'Unauthorized: Access is denied due to invalid credentials'
            else:
                error_message = HTTPStatus(response.status_code).phrase
            return error_message
        except:
            return response.text or error_message
