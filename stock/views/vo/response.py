class Response(object):
    def __init__(self, code=200, msg='成功', body=None):
        self.code = code
        self.msg = msg
        self.body = body
