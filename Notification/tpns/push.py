import json
from typing import Dict, List, BinaryIO
from tpns.core.authenticators import Authenticator, BasicAuthenticator
from tpns.core import BaseService, APIResponse
from tpns.common import (
    get_sdk_headers,
    ZONE_GZ, ZONES,
    ENDPOINT_PUSH,
    ENDPOINT_ADD_PLAN_PUSH,
    ENDPOINT_UPLOAD_PACKAGE,
)
from tpns.core.utils import (
    remove_null_values,
    merge_params
)


class Push(BaseService):
    """The  Push service."""

    # audience_type
    AUDIENCE_TYPE_ALL = 'all'
    AUDIENCE_TYPE_TAG = 'tag'
    AUDIENCE_TYPE_TOKEN = 'token'
    AUDIENCE_TYPE_TOKEN_LIST = 'token_list'
    AUDIENCE_TYPE_ACCOUNT = 'account'
    AUDIENCE_TYPE_ACCOUNT_LIST = 'account_list'
    AUDIENCE_TYPE_PACKAGE_ACCOUNT_PUSH = 'package_account_push'
    AUDIENCE_TYPE_PACKAGE_TOKEN_PUSH = 'package_token_push'

    def __init__(
            self,
            zone: str = ZONE_GZ,
            authenticator: Authenticator = None,
    ) -> None:
        """
        Construct a new client for the Push service.
        :param str zone: The zone where the application is deployed. Defaults to gz.
        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
        """
        if not authenticator:
            raise ValueError('authenticator must be provided')

        if not isinstance(authenticator, BasicAuthenticator):
            raise ValueError('authenticator only support basic auth now')
        self.zone = zone
        BaseService.__init__(self, authenticator=authenticator)

    #########################
    # push
    #########################
    def push(self,
             audience_type: str = None, message: 'Message' = None, message_type: str = 'notify',
             environment: str = None, upload_id: int = None, expire_time: int = None, send_time: str = None,
             multi_pkg: bool = None, loop_param: Dict = None, group_id: str = None, plan_id: str = None,
             tag_rules: List[Dict] = None, account_list: List[str] = None, account_push_type: int = None,
             account_type: int = None,
             token_list: List[str] = None, push_speed: int = None, collapse_id: int = None,
             channel_rules: List[Dict] = None,
             tpns_online_push_type: int = None, force_collapse: bool = None, extend_params: Dict = None,
             ignore_invalid_token: int = None,
             **kwargs) -> APIResponse:

        if audience_type is None:
            raise ValueError('audience_type must be provided')
        if audience_type == self.AUDIENCE_TYPE_TAG and tag_rules is None:
            raise ValueError('tag_rules must be provided')
        if (audience_type == self.AUDIENCE_TYPE_TOKEN or audience_type == self.AUDIENCE_TYPE_TOKEN) \
                and token_list is None:
            raise ValueError('token_list must be provided')
        if (audience_type == self.AUDIENCE_TYPE_ACCOUNT or audience_type == self.AUDIENCE_TYPE_ACCOUNT_LIST) \
                and account_list is None:
            raise ValueError('account_list must be provided')
        if message is None:
            raise ValueError('message must be provided')
        if (audience_type == Push.AUDIENCE_TYPE_PACKAGE_ACCOUNT_PUSH or
            audience_type == Push.AUDIENCE_TYPE_PACKAGE_TOKEN_PUSH) \
                and upload_id is None:
            raise ValueError('upload_id must be provided')

        data = {
            'audience_type': audience_type,
            'message': message,
            'message_type': message_type,
            'environment': environment,
            'upload_id': upload_id,
            'expire_time': expire_time,
            'send_time': send_time,
            'multi_pkg': multi_pkg,
            'loop_param': loop_param,
            'group_id': group_id,
            'plan_id': plan_id,
            'tag_rules': tag_rules,
            'account_list': account_list,
            'account_push_type': account_push_type,
            'account_type': account_type,
            'token_list': token_list,
            'push_speed': push_speed,
            'collapse_id': collapse_id,
            'channel_rules': channel_rules,
            'tpns_online_push_type': tpns_online_push_type,
            'force_collapse': force_collapse,
            'ignore_invalid_token': ignore_invalid_token,
        }

        merge_params(data, extend_params)
        data = remove_null_values(data)
        data = json.dumps(data)

        headers = get_sdk_headers('push')
        headers['content-type'] = 'application/json'
        url = ZONES[self.zone][ENDPOINT_PUSH]
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)
        response = self.send(request, **kwargs)
        return response

    #########################
    # Add plan push
    #########################
    def add_plan_push(self, plan_name: str = None, plan_describe: str = None, extend_params: Dict = None,
                      **kwargs) -> APIResponse:
        if plan_name is None:
            raise ValueError('plan_name must be provided')
        if plan_describe is None:
            raise ValueError('plan_describe must be provided')
        data = {
            'planName': plan_name,
            'planDescribe': plan_describe
        }
        merge_params(data, extend_params)
        data = remove_null_values(data)
        headers = get_sdk_headers('add_plan_push')
        headers['content-type'] = 'application/json'
        url = ZONES[self.zone][ENDPOINT_ADD_PLAN_PUSH]
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=json.dumps(data))
        response = self.send(request, **kwargs)
        return response

    #########################
    # Upload package
    #########################
    def upload_package(self, file: BinaryIO, file_content_type: str = None, **kwargs) -> APIResponse:
        if file is None:
            raise ValueError('file must be provided')
        headers = get_sdk_headers('upload_package')
        headers['Accept'] = 'application/json'
        url = ZONES[self.zone][ENDPOINT_UPLOAD_PACKAGE]

        form_data = [('file', (None, file, file_content_type or
                               'application/octet-stream'))]
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       files=form_data)

        response = self.send(request)
        return response


class Message(object):
    def __init__(self, title: str = None, content: str = None, thread_id: str = None, xg_media_resources: str = None,
                 **kwargs) -> None:
        self.title = title
        self.content = content
        self.thread_id = thread_id
        self.xg_media_resources = xg_media_resources
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)


class iOSMessage(Message):
    def __init__(self,
                 ios: 'iOS' = None,
                 ) -> None:
        self.ios = ios


class iOS(object):
    def __init__(self, aps: 'Aps' = None, custom_content: str = None, xg: str = None) -> None:
        self.aps = aps
        self.custom_content = custom_content
        self.xg = xg


class Aps(object):
    def __init__(self, alert: Dict = None, badge_type: int = None, category: str = None, mutable_content: int = None,
                 sound: str = None) -> None:
        self.alert = alert
        self.badge_type = badge_type
        self.category = category
        self.mutable_content = mutable_content
        self.sound = sound


class AndroidMessage(Message):
    def __init__(self, accept_time: List[Dict] = None,
                 thread_sumtext: str = None, xg_media_resources: str = None,
                 xg_media_audio_resources: str = None, android: 'Android' = None) -> None:
        self.accept_time = accept_time
        self.thread_sumtext = thread_sumtext
        self.xg_media_resources = xg_media_resources
        self.xg_media_audio_resources = xg_media_audio_resources
        self.android = android


class Android(object):
    def __init__(self, n_ch_id: str = None, n_ch_name: str = None, xm_ch_id: str = None,
                 hw_ch_id: str = None, oppo_ch_id: str = None, vivo_ch_id: str = None, n_id: int = None,
                 builder_id: int = None, badge_type: int = None, ring: int = None, ring_raw: int = None,
                 vibrate: int = None, lights: int = None, clearable: int = None, icon_type: int = None,
                 icon_res: str = None,
                 style_id: int = None, small_icon: str = None, icon_color: int = None, action: 'Action' = None,
                 custom_content: str = None, show_type: int = None, **kwargs) -> None:
        self.n_ch_id = n_ch_id
        self.n_ch_name = n_ch_name
        self.xm_ch_id = xm_ch_id
        self.hw_ch_id = hw_ch_id
        self.oppo_ch_id = oppo_ch_id
        self.vivo_ch_id = vivo_ch_id
        self.n_id = n_id
        self.builder_id = builder_id
        self.badge_type = badge_type
        self.ring = ring
        self.ring_raw = ring_raw
        self.vibrate = vibrate
        self.lights = lights
        self.clearable = clearable
        self.icon_type = icon_type
        self.icon_res = icon_res
        self.style_id = style_id
        self.small_icon = small_icon
        self.icon_color = icon_color
        self.action = action
        self.custom_content = custom_content
        self.show_type = show_type
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)


class Action(object):
    def __init__(self, action_type: int = None, activity: str = None, aty_attr: Dict = None, browser: Dict = None,
                 intent: str = None, **kwargs) -> None:
        self.action_type = action_type
        self.activity = activity
        self.aty_attr = aty_attr
        self.browser = browser
        self.intent = intent
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)
