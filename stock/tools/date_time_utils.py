from datetime import datetime


class date_time(object):

    @staticmethod
    def converter_time(obj, fmt='%Y-%m-%d %H:%M:%S'):
        if isinstance(obj, datetime):
            return obj.strftime(fmt)
