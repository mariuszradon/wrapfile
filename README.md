# wrapfile

Wrappers for file-like objects.

Simplifies writing functions that can take as an argument 'buffer'
a file-like or a path-like object. If the argument was already a file,
it is just wrapped; if it is a string or path-like object, the file is
open and wrapped. Finally, if the argument is None (which is the
default for TextFileWriter) a StringIO object is created to which the
data are written in memory and can be returned using getvalue()
method. Otherwise, getvalue() return None.

```python
from wrapfile import TextFileWriter
def say_hello(buf=None):
    """Just say 'Hello, world!'

    Parameters:
    -----------
    buf : file-like or path-like, optional
         buffer to write to. If None, the output will be returned.

    Returns:
    --------
    str or None:
         the output if the argument was omitted,
         or None otherwise.
    """
    with TextFileWriter(buf) as f:
        f.write("Hello, world!")
    if f.has_value:
        return f.getvalue()

# usage:
# - with no argument
print(say_hello())

# - with a path-like object
say_hello('myfile.txt')

# - with a file-like object
with open('myfile.txt', 'w') as f:
    say_hello(f)

def myfunc(buf):
    """Print the contents of buffer

    Parameters:
    -----------
    buf : file-like or path-like
         buffer to read from
    """
    with TextFileReader(buf) as f:
        result = f.read()
    print(result)

# usage:
# - with a path-like object
print(myfunc('myfile.txt')

# - with a file-like object
with open('myfile.txt', 'r') as f:
    print(myfunc(f))
```
