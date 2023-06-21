import logging
import requests
import platform
import sys
import json as json_import
from os.path import basename
from ..version import __version__
from http.cookiejar import CookieJar
from typing import Dict, List, Optional, Tuple, Union
from requests.structures import CaseInsensitiveDict
from .authenticators import Authenticator
from .api_response import APIResponse
from .api_exception import ApiException
from .utils import (
    remove_null_values,
    cleanup_values,
    strip_extra_slashes
)


class BaseService:
    """Common functionality shared by generated service classes.

    The base service authenticates requests via its authenticator, stores cookies, and
    wraps responses from the service endpoint in DetailedResponse or APIException objects.

    Keyword Arguments:
        authenticator: Adds authentication data to service requests. Defaults to None.
        disable_ssl_verification: A flag that indicates whether verification of the server's SSL
            certificate should be disabled or not. Defaults to False.
        enable_gzip_compression: A flag that indicates whether to enable gzip compression on request bodies

    Attributes:
        authenticator (Authenticator): Adds authentication data to service requests.
        disable_ssl_verification (bool): A flag that indicates whether verification of
            the server's SSL certificate should be disabled or not.
        default_headers (dict): A dictionary of headers to be sent with every HTTP request to the service endpoint.
        jar (http.cookiejar.CookieJar): Stores cookies received from the service.
        http_config (dict): A dictionary containing values that control the timeout, proxies, and etc of HTTP requests.
        enable_gzip_compression (bool): A flag that indicates whether to enable gzip compression on request bodies
    Raises:
        ValueError: If Authenticator is not provided or invalid type.
    """

    SDK_NAME = 'tpns-python-sdk'

    ERROR_MSG_DISABLE_SSL = 'The connection failed because the SSL certificate is not valid. To use a self-signed ' \
                            'certificate, disable verification of the server\'s SSL certificate by invoking the ' \
                            'set_disable_ssl_verification(True) on your service instance and/ or use the ' \
                            'disable_ssl_verification option of the authenticator.'

    def __init__(self,
                 *,
                 authenticator: Authenticator = None,
                 disable_ssl_verification: bool = False,
                 enable_gzip_compression: bool = False) -> None:
        self.http_config = {}
        self.jar = CookieJar()
        self.authenticator = authenticator
        self.disable_ssl_verification = disable_ssl_verification
        self.default_headers = None
        self.enable_gzip_compression = enable_gzip_compression
        self._set_user_agent_header(self._build_user_agent())
        if not self.authenticator:
            raise ValueError('authenticator must be provided')
        if not isinstance(self.authenticator, Authenticator):
            raise ValueError(
                'authenticator should be of type Authenticator')

    @staticmethod
    def _get_system_info() -> str:
        return '{0} {1} {2}'.format(
            platform.system(),  # OS
            platform.release(),  # OS version
            platform.python_version()  # Python version
        )

    def _build_user_agent(self) -> str:
        return '{0}-{1} {2}'.format(self.SDK_NAME, __version__,
                                    self._get_system_info())

    def _set_user_agent_header(self, user_agent_string: str) -> None:
        self.user_agent_header = {'User-Agent': user_agent_string}

    def set_disable_ssl_verification(self, status: bool = False) -> None:
        """Set the flag that indicates whether verification of
        the server's SSL certificate should be disabled or not.

        Keyword Arguments:
            status: set to true to disable ssl verification (default: {False})
        """
        self.disable_ssl_verification = status

    # def set_service_url(self, service_url: str) -> None:
    #     """Set the url the service will make HTTP requests too.
    #
    #     Arguments:
    #         service_url: The WHATWG URL standard origin ex. https://example.service.com
    #
    #     Raises:
    #         ValueError: Improperly formatted service_url
    #     """
    #     if has_bad_first_or_last_char(service_url):
    #         raise ValueError(
    #             'The service url shouldn\'t start or end with curly brackets or quotes. '
    #             'Be sure to remove any {} and \" characters surrounding your service url'
    #         )
    #     self.service_url = service_url

    def get_authenticator(self) -> Authenticator:
        """Get the authenticator currently used by the service.

        Returns:
            The authenticator currently used by the service.
        """
        return self.authenticator

    def set_default_headers(self, headers: Dict[str, str]) -> None:
        """Set http headers to be sent in every request.

        Arguments:
            headers: A dictionary of headers
        """
        if isinstance(headers, dict):
            self.default_headers = headers
        else:
            raise TypeError("headers parameter must be a dictionary")

    def send(self, request: requests.Request, **kwargs) -> APIResponse:
        """Send a request and wrap the response in a DetailedResponse or APIException.

        Args:
            request: The request to send to the service endpoint.

        Raises:
            ApiException: The exception from the API.

        Returns:
            The response from the request.
        """
        # Use a one minute timeout when our caller doesn't give a timeout.
        # http://docs.python-requests.org/en/master/user/quickstart/#timeouts
        kwargs = dict({"timeout": 60}, **kwargs)
        kwargs = dict(kwargs, **self.http_config)

        if self.disable_ssl_verification:
            kwargs['verify'] = False

        # Check to see if the caller specified the 'stream' argument.
        stream_response = kwargs.get('stream') or False

        try:
            print(request)
            response = requests.request(**request, cookies=self.jar, **kwargs)

            if 200 <= response.status_code <= 299:
                if response.status_code == 204 or request['method'] == 'HEAD':
                    # There is no body content for a HEAD request or a 204 response
                    result = None
                elif stream_response:
                    result = response
                elif not response.text:
                    result = None
                else:
                    try:
                        result = response.json()
                    except:
                        result = response
                return APIResponse(response=result, headers=response.headers,
                                   status_code=response.status_code)

            raise ApiException(
                response.status_code, http_response=response)
        except requests.exceptions.SSLError:
            logging.exception(self.ERROR_MSG_DISABLE_SSL)
            raise
        except ApiException as err:
            logging.exception(err.message)
            raise
        except:
            logging.exception('Error in service call')
            raise

    def prepare_request(self,
                        method: str,
                        url: str,
                        *,
                        headers: Optional[dict] = None,
                        params: Optional[dict] = None,
                        data: Optional[Union[str, dict]] = None,
                        files: Optional[Union[
                            Dict[str, Tuple[str]],
                            List[Tuple[str, Tuple[str, ...]]]
                        ]] = None) -> dict:
        """Build a dict that represents an HTTP service request.

        Clean up headers, add default http configuration, convert data
        into json, process files, and merge all into a single request dict.

        Args:
            method: The HTTP method of the request ex. GET, POST, etc.
            url: The origin + pathname according to WHATWG spec.

        Keyword Arguments:
            headers: Headers of the request.
            params: Querystring data to be appended to the url.
            data: The request body. Converted to json if a dict.
            files: 'files' can be a dictionary (i.e { '<part-name>': (<tuple>)}),
                or a list of tuples [ (<part-name>, (<tuple>))... ]

        Returns:
            Prepared request dictionary.
        """
        # pylint: disable=unused-argument; necessary for kwargs
        request = {'method': method}

        # validate the service url is set
        if not url:
            raise ValueError('The url is required')
        request['url'] = strip_extra_slashes(url)

        headers = remove_null_values(headers) if headers else {}
        headers = cleanup_values(headers)
        headers = CaseInsensitiveDict(headers)
        if self.default_headers is not None:
            headers.update(self.default_headers)
        if 'user-agent' not in headers:
            headers.update(self.user_agent_header)
        request['headers'] = headers

        if params and isinstance(params, dict):
            params = remove_null_values(params)
            params = cleanup_values(params)
            request['params'] = params

        if sys.version_info >= (3, 0) and isinstance(data, str):
            data = data.encode('utf-8')

        if data and isinstance(data, dict):
            data = remove_null_values(data)
            if headers.get('content-type') is None:
                headers.update({'content-type': 'application/json'})
            data = json_import.dumps(data)
        request['data'] = data

        self.authenticator.authenticate(request)

        # Next, we need to process the 'files' argument to try to fill in
        # any missing filenames where possible.
        # 'files' can be a dictionary (i.e { '<part-name>': (<tuple>)} )
        # or a list of tuples [ (<part-name>, (<tuple>))... ]
        # If 'files' is a dictionary we'll convert it to a list of tuples.
        new_files = []
        if files is not None:
            # If 'files' is a dictionary, transform it into a list of tuples.
            if isinstance(files, dict):
                files = remove_null_values(files)
                files = files.items()
            # Next, fill in any missing filenames from file tuples.
            for part_name, file_tuple in files:
                if file_tuple and len(file_tuple) == 3 and file_tuple[0] is None:
                    file = file_tuple[1]
                    if file and hasattr(file, 'name'):
                        filename = basename(file.name)
                        file_tuple = (filename, file_tuple[1], file_tuple[2])
                new_files.append((part_name, file_tuple))
        request['files'] = new_files
        return request

    @staticmethod
    def encode_path_vars(*args: str) -> List[str]:
        """Encode path variables to be substituted into a URL path.

        Arguments:
            args: A list of strings to be URL path encoded

        Returns:
            A list of encoded strings that are safe to substitute into a URL path.
        """
        return (requests.utils.quote(x, safe='') for x in args)

    # The methods below are kept for compatibility and should be removed
    # in the next major release.

    # pylint: disable=protected-access

    @staticmethod
    def _convert_model(val: str) -> None:
        if isinstance(val, str):
            val = json_import.loads(val)
        if hasattr(val, "_to_dict"):
            return val._to_dict()
        return val

    @staticmethod
    def _convert_list(val: list) -> None:
        if isinstance(val, list):
            return ",".join(val)
        return val

    @staticmethod
    def _encode_path_vars(*args) -> None:
        return (requests.utils.quote(x, safe='') for x in args)
