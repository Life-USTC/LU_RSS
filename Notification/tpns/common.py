import platform
from .version import __version__

USER_AGENT_HEADER = 'User-Agent'
SDK_NAME = 'tpns-python-sdk'
SDK_API_HEADER = 'X-TPNS-API'

# area
ZONE_GZ = 'gz'
ZONE_SH = 'sh'
ZONE_HK = 'hk'
ZONE_SGP = 'sgp'

# url
URL_GZ = 'https://api.tpns.tencent.com/v3'
URL_SH = 'https://api.tpns.sh.tencent.com/v3'
URL_HK = 'https://api.tpns.hk.tencent.com/v3'
URL_SGP = 'https://api.tpns.sgp.tencent.com/v3'

# endpoint
ENDPOINT_PUSH = '/push/app'
ENDPOINT_ADD_PLAN_PUSH = '/push/plan/add_plan_push'
ENDPOINT_UPLOAD_PACKAGE = '/push/package/upload'

# message type
MESSAGE_TYPE_NOTIFY = 'notify'
MESSAGE_TYPE_MESSAGE = 'message'


def get_system_info():
    return '{0} {1} {2}'.format(
        platform.system(),  # OS
        platform.release(),  # OS version
        platform.python_version())  # Python version


user_agent = '{0}-{1} {2}'.format(SDK_NAME, __version__, get_system_info())


def get_user_agent():
    return user_agent


def get_sdk_headers(api_name: str = None):
    headers = {USER_AGENT_HEADER: get_user_agent(), SDK_API_HEADER: api_name}
    return headers


ZONES = {
    # 广州
    ZONE_GZ: {
        ENDPOINT_PUSH: '{0}{1}'.format(URL_GZ, ENDPOINT_PUSH),
        ENDPOINT_ADD_PLAN_PUSH: '{0}{1}'.format(URL_GZ, ENDPOINT_ADD_PLAN_PUSH),
        ENDPOINT_UPLOAD_PACKAGE: '{0}{1}'.format(URL_GZ, ENDPOINT_UPLOAD_PACKAGE),
    },
    # 上海
    ZONE_SH: {
        ENDPOINT_PUSH: '{0}{1}'.format(URL_SH, ENDPOINT_PUSH),
        ENDPOINT_ADD_PLAN_PUSH: '{0}{1}'.format(URL_SH, ENDPOINT_ADD_PLAN_PUSH),
        ENDPOINT_UPLOAD_PACKAGE: '{0}{1}'.format(URL_SH, ENDPOINT_UPLOAD_PACKAGE),
    },
    # 香港
    ZONE_HK: {
        ENDPOINT_PUSH: '{0}{1}'.format(URL_HK, ENDPOINT_PUSH),
        ENDPOINT_ADD_PLAN_PUSH: '{0}{1}'.format(URL_HK, ENDPOINT_ADD_PLAN_PUSH),
        ENDPOINT_UPLOAD_PACKAGE: '{0}{1}'.format(URL_HK, ENDPOINT_UPLOAD_PACKAGE),
    },
    # 新加坡
    ZONE_SGP: {
        ENDPOINT_PUSH: '{0}{1}'.format(URL_SGP, ENDPOINT_PUSH),
        ENDPOINT_ADD_PLAN_PUSH: '{0}{1}'.format(URL_SGP, ENDPOINT_ADD_PLAN_PUSH),
        ENDPOINT_UPLOAD_PACKAGE: '{0}{1}'.format(URL_SGP, ENDPOINT_UPLOAD_PACKAGE),
    }
}
