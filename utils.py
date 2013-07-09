# Object to test for something missing, where None cannot be used because it is
# a valid value.
_missing = object()


class Enum(set):
    """Simple enum implementation."""
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
