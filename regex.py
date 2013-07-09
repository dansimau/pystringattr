import re

# Splits a syntax string into attribute components.
#
# Eg.:
#   'foo.bar[2].baz'
#
# Becomes:
#   'foo'
#   'bar'
#   '[2]'
#   'baz'
#
RE_SPLIT = re.compile(r'\.|(\[[\'"]?\w+[\'"]?\])')

# Extracts a string-based key from between square brackets
#
# Eg.:
#   '["foo"]'
#
# Has a group component of:
#   'foo'
#
RE_KEY = re.compile(r'\[[\'"](\w+)[\'"]\]')

# Extracts an integer based index from between square brackets
#
# Eg.:
#   '[2]'
#
# Has a group component of:
#   '2'
#
RE_INDEX = re.compile(r'\[\d\]')
