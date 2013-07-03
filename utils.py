class _Missing(object):
    """Object to test for something missing, where None cannot be used
    because it is a valid value.
    """
    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
