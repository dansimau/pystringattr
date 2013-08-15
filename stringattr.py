import re
from collections import namedtuple, deque

from .regex import RE_SPLIT, RE_KEY, RE_INDEX
from .utils import Enum, _missing


StackItem = namedtuple('StackItem', ['name', 'access_method'])

# Accessor methods:
# INDEX means this accessor is index or key-based, eg. [1] or ['foo']
# DEFAULT means property
AccessorType = Enum(['INDEX', 'DEFAULT'])


def first(*vals):
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
    except (KeyError, IndexError, TypeError):
        return _missing


def get_attribute(obj, attr):
    """Retrieve attribute from the specified obj, or return
    _missing if it does not exist.
    """
    try:
        return getattr(obj, attr)
    except AttributeError:
        return _missing


class StringAttribute(object):
    """
    Used to access a deeply nested attributes of a Python data structure
    using a string representation of Python-like syntax.

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
    StringAttribute('foo.bar[1].baz').get(my_dict)
    """

    def __init__(self, string_attr_path=None, default=_missing):
        self._default = default
        if string_attr_path is not None:
            self._stack = self._parse(string_attr_path)
        self._string_attr_path = string_attr_path

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._string_attr_path)

    def __str__(self):
        return '%r' % self._string_attr_path

    def _get(self, obj, stack, default=_missing):
        """Retrieve value from an object structure given a list of
        attributes."""
        pointer = obj

        # Try all access methods
        for accessor in stack:

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
                if default is not _missing:
                    return default
                else:
                    self._raise_exception(obj, accessor.name)

        return pointer

    def _parse(self, string_attr_path):
        """Parse string_attr_path into a stack of accessors."""
        stack = deque()

        for node in self._split(string_attr_path):

            # Node is a list index (eg. '[2]')
            if re.match(RE_INDEX, node):
                # Convert into integer
                list_index = int(node.translate(None, '[]'))
                stack.append(StackItem(list_index, AccessorType.INDEX))

            # Node is a key (string-based index)
            elif re.match(RE_KEY, node):
                key = re.match(RE_KEY, node).groups()[0]
                stack.append(StackItem(key, AccessorType.INDEX))

            else:
                # Default accessor method
                stack.append(StackItem(node, AccessorType.DEFAULT))

        return stack

    def _raise_exception(self, obj, node):
        """Raise exception."""
        raise Exception('%r object has no key or attribute at path %r' % (obj.__class__.__name__, node))

    @classmethod
    def _split(cls, string_attr_path):
        """Split string into list of accessor nodes."""
        # Split string at '.' and '[0]'
        nodes = re.split(RE_SPLIT, string_attr_path)
        # Filter out empty position params from the split
        nodes = filter(lambda x: x, nodes)
        return nodes

    def get(self, obj, string_attr_path=None, default=_missing):
        """Retrieve value from an object structure using string
        representation of attributes path."""

        # Get defaults
        if default is _missing:
            default = self._default

        if string_attr_path is not None:
            stack = self._parse(string_attr_path)
        else:
            string_attr_path = self._string_attr_path
            stack = self._stack

        return self._get(obj, stack, default)


    def set(self, base_obj, value, string_attr_path=None):
        """Set value on an object structure using string representation
        of attributes path."""
        if string_attr_path is not None:
            stack = self._parse(string_attr_path)
        else:
            string_attr_path = self._string_attr_path
            stack = self._stack

        # Get the name of the attribute we're setting (the last item in
        # the stack)
        attr = stack.pop()

        # Get the actual object we're going to operate on
        target_obj = self._get(base_obj, stack)

        # Set the attribute or key value
        if attr.access_method == AccessorType.INDEX:
            target_obj[attr.name] = value
        else:
            setattr(target_obj, attr.name, value)


# Wrapper functions for a builtin-esque feel...

def getstrattr(obj, attr, default=_missing):
    """Retrieve value from an object structure using string
    representation of attributes path."""
    return StringAttribute().get(obj, attr, default)

def setstrattr(obj, attr, val):
    """Set value on an object structure using string representation
    of attributes path."""
    return StringAttribute().set(obj, val, attr)
