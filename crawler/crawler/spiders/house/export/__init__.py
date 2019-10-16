import os


class export(object):
    @staticmethod
    def export_path():
        module_path = os.path.dirname(__file__)
        return module_path
