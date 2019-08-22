

class serialize_generic(object):

    @classmethod
    def serialize(cls, object_dict):
        obj = cls()
        obj.__dict__.update(object_dict)
        return obj

    @classmethod
    def revers_serialize(cls):
        return None
