#!/usr/bin/env python3

import string

# 1. % Operator
name = 'Frank'
errno = 101
print('Hello, %s' % name)
print('Hey %s, there is a 0x%x error!' % (name, errno))
print('Hey %(name)s, there is a 0x%(errno)x error!' % {"name": name, "errno": errno})

# 2.String Formatting (format)
print('Hello, %s'.format(name))
print('Hey {name}s, there is a 0x{errno:x} error!'.format(name=name, errno=errno))

# 3.  f-Strings
# embedded python expression
a = 5
b = 7
print(f'Hello, {name}!')
print(f'Five plus ten is {a + b} and not {2 * (a + b)}.')

# 4. Templates string
print(string.Template('Hey $name').substitute(name=name))

log_template = string.Template("""
Hello $name,
Errno $errno
""")

logValue = {"name": name, "errno":errno}

print(log_template.substitute(logValue))
