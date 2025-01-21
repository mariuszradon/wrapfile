# wrapfile

FileWrapper, TextFileReader and TextFileWriter are used to construct a
file-like object from a file-like object, a path or None (to indicate
a memory buffer). The resulting wrapper redirects most of the methods
to the actual file object. The close() method of the wrapper closes
the actual file only when it was opened when constructing the wrapper
(based on the provided file path) or if the memory buffer was created.

The purpose is to simplify writing functions that can take as an
argument a 'filepath_or_buffer' which can be string, path object, a
file-like object or None:

- If the argument is file-like, it is simply wrapped to perform the
actual I/O operations.

- If the argument is str or path object, it is treated as path of the
file to be opened and managed (the user does not have to bother about
closing the internal file).

- If the argument None, an empty in-memory buffer is created
(io.BytesIO or io.StringIO) to which data can be written. The written
data can be returned back using the getvalue() implemented in
TextFileWriter.

##Example
```python
from wrapfile import TextFileWriter
def say_hello(filepath_or_buffer=None):
    """Just say 'Hello, world!'

    Parameters:
    -----------
    filepath_or_buffer : str, path or file-like object, optional
         A file to save the output.
         If None, the output will be returned.

    Returns:
    --------
    str or None:
         the output if the argument was omitted,
         or None otherwise.
    """
    with TextFileWriter(filepath_or_buffer) as f:
        f.write("Hello, world!")
        result = f.getvalue()
    return result

# usage:
# - with no argument
print(say_hello())

# - with a str or path-like object
say_hello('myfile.txt')

# - with a file-like object
with open('myfile.txt', 'w') as f:
    say_hello(f)

from wrapfile import TextFileReader
import sys
def read_from(filepath_or_buffer=sys.stdin):
    """Read from the file or standard input

    Parameters:
    -----------
    filepath_or_buffer : str, path or file-like object, optional
         A file to read the input from.
         The default is to read from the standard input (sys.stdin).

    Returns:
    --------
    str : 
        The file contents.
    """
    with TextFileReader(filepath_or_buffer) as f:
        result = f.read()
    return result

# usage:
# - with the standard input
print(read_from())

# - with another file-like object
with open('myfile.txt', 'r') as f:
    print(read_from(f))

# - with a str or path-like object
print(read_from('myfile.txt')

```
