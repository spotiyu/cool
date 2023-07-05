# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Resource
from flask_restful import reqparse

from routings.live_api_routing import RunScripts

live_api = Blueprint('live_api', __name__)

# 响应模板
return_model = {'state': 0, 'data': None}

class LiveUrl(Resource):
    """
    直播流接口
    """

    def __init__(self):
        self.return_data = return_model
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('pt', type=str, required=True, help='平台')
        self.reqparse.add_argument('aid', type=str, required=True, help='id')
        super(LiveUrl, self).__init__()

    def get(self):
        # 定义消息体
        return_data = self.return_data.copy()
        # 接收front参数
        args = self.reqparse.parse_args()
        pt = args.get('pt')
        aid = args.get('aid')
        live_url = RunScripts(pt, aid).choice()
        if not live_url:
            return return_data
        return_data['state'] = 1
        return_data['data'] = live_url
        return return_data


live_api.add_url_rule(rule='/jx', view_func=LiveUrl.as_view('get-live-url'))
