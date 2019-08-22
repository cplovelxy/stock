import json

from stock.tools.date_time_utils import date_time


class Response(object):
    def __init__(self, code=200, msg='成功', body=None):
        self.code = code
        self.msg = msg
        self.body = body

    @staticmethod
    def succeed(body=None):
        return json.dumps(Response(body=body).__dict__, ensure_ascii=False, default=date_time.converter_time)
