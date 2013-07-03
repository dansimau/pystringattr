import re
from collections import namedtuple, deque

from .utils import Enum, _missing


SPLIT_RE = re.compile(r'\.|(\[[\'"]?\w+[\'"]?\])')
KEY_RE = re.compile(r'\[[\'"](\w+)[\'"]\]')
INDEX_RE = re.compile(r'\[\d\]')

StackItem = namedtuple('StackItem', ['name', 'access_method'])

# Accessor methods:
# INDEX means this accessor is index or key-based, eg. [1] or ['foo']
# DEFAULT means property
AccessorType = Enum(['INDEX', 'DEFAULT'])


def first(cls, *vals):
    """Return the first value that's not _missing."""
    for val in vals:
        if val is not _missing:
            return val
    return _missing


def get_key(obj, index):
    """Retrieve index or key from the specified obj, or return
    _missing if it does not exist.
    """
    try:
        return obj[index]
    except (KeyError, IndexError):
        return _missing


def get_attribute(obj, attr):
    """Retrieve attribute from the specified obj, or return
    _missing if it does not exist.
    """
    try:
        return getattr(obj, attr)
    except AttributeError:
        return _missing


class JSONNotation(object):
    """
    Used to access a deeply nested attributes of a Python data structure
    using JSON notation.

    Eg.:

    # Data structure
    my_dict = {
        'foo': {
            'bar': [
                {'baz': 'wee'},
                {'baz': 'woo'}
            ]
        }
    }

    # Return 'woo'
    JSONNotation('foo.bar[1].baz').apply(my_dict)
    """

    def __init__(self, notation=None, default=None, strict=False):
        self._default = default
        self._strict = strict
        if notation is not None:
            self._parse(notation)

    def __repr__(self):
        return '%s(\'%s\')' % (self.__class__.__name__, self._notation)

    def __str__(self):
        return '%r' % self._notation

    def _parse(self, notation):
        """Parse notation into a stack of accessors."""
        self._notation = notation
        self._stack = deque()

        for node in self._split(notation):

            # Node is a list index (eg. '[2]')
            if re.match(INDEX_RE, node):
                # Convert into integer
                list_index = int(node.translate(None, '[]'))
                self._stack.append(StackItem(list_index, AccessorType.INDEX))

            # Node is a key (string-based index)
            elif re.match(KEY_RE, node):
                key = re.match(KEY_RE, node).groups()[0]
                self._stack.append(StackItem(key, AccessorType.INDEX))

            else:
                # Default accessor method
                self._stack.append(StackItem(node, AccessorType.DEFAULT))

    def _raise_exception(self, node):
        """Raise exception."""
        raise Exception('Node %r not found' % node)

    @classmethod
    def _split(cls, notation):
        """Split notation string into list of accessor nodes."""
        # Split string at '.' and '[0]'
        nodes = re.split(SPLIT_RE, notation)
        # Filter out empty position params from the split
        nodes = filter(lambda x: x, nodes)
        return nodes

    def apply(self, obj, notation=None, default=_missing, strict=None):
        """Retrieve value from an object structure using notation."""

        # Get defaults
        if notation is None:
            notation = self._notation
        if default is _missing:
            default = self._default
        if strict is None:
            strict = self._strict

        # Set up pointer at root level object
        pointer = obj

        for accessor in self._stack:

            # Key or index accessors
            if accessor.access_method == AccessorType.INDEX:
                pointer = get_key(pointer, accessor.name)

            # Default accessor
            elif accessor.access_method == AccessorType.DEFAULT:

                # Attempt to get the object attribute first, or if that fails
                # try to get a key with that name or list index
                pointer = first(get_attribute(pointer, accessor.name),
                                get_key(pointer, accessor.name))

            # If nothing could be accessed return None or raise an error
            if pointer is _missing:
                if not strict:
                    return default
                else:
                    self._raise_exception(accessor.name)

        return pointer
