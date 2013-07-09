"""
Used to access a deeply nested attributes of a Python data structure
using string representation of Python-like syntax.

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
StringAttribute('foo.bar[1].baz').apply(my_dict)

# By default, missing attributes in the path will return None:

# Returns None
StringAttribute('foo.bar.id').apply(my_dict)

# If you want to raise errors instead:
StringAttribute('foo.bar.id').apply(my_dict, strict=True)

# Default return can be specified (when strict=False):

# Returns False
StringAttribute('foo.bar.id').apply(my_dict, default=False)

# Parse once, apply many times
j = StringAttribute('foo.bar[0].baz', default=False)
j.apply(my_dict)

# Use one instance to apply arbitrary notations
j = StringAttribute()
j.apply(my_dict, 'foo.bar')
"""
from .stringattr import StringAttribute

__all__ = ['StringAttribute']
