"""
Used to access a deeply nested attributes of a Python data structure
using JSON-like notation.

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

# Returns 'woo'
JSONNotation('foo.bar[1].baz').apply(my_dict)

# By default, missing attributes in the path will return None:

# Returns None
JSONNotation('foo.bar.id').apply(my_dict)

# If you want to raise errors instead:
JSONNotation('foo.bar.id').apply(my_dict, strict=True)

# Default return can be specified (when strict=False):

# Returns False
JSONNotation('foo.bar.id').apply(my_dict, default=False)

# Parse once, apply many times
j = JSONNotation('foo.bar[0].baz', default=False)
j.apply(my_dict)

# Use one instance to apply arbitrary notations
j = JSONNotation()
j.apply(my_dict, 'foo.bar')
"""
from .jsonnotation import JSONNotation

__all__ = ['JSONNotation']
