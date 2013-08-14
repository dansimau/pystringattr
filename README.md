stringattr
==========

Used to access a deeply nested attributes of a Python data structure
using string representation of Python-like syntax.

Example
-------

Define a data structure in Python using dicts and lists:

    my_dict = {
        'foo': {
            'bar': [
                {'baz': 'wee'},
                {'baz': 'woo'}
            ]
        }
    }

Return a deeply nested value:

    # Returns 'woo'
    getstrattr(my_dict, 'foo.bar[1].baz')

By default, missing attributes in the path will raise an exception
unless the value of `default` is set:

    # Raises an exception
    getatrattr(my_dict, 'foo.bar.id')

    # Returns None
    getatrattr(my_dict, 'foo.bar.id', default=None)

    # Returns False
    getatrattr(my_dict, 'foo.bar.id', default=False)

Parse/save attribute string once, then get many times:

    j = StringAttribute('foo.bar[0].baz', default=None)
    j.get(my_dict)
