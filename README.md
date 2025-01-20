# wrapfile

Wrappers for file-like objects.

Simplifies writing functions that can take as argument either a file-like or path-like object.

```python
from wrapfile import TextFileWriter
def myfunc_write(buf):
    """Write 'Hello, world!' to buffer

    Parameters:
    -----------
    buf : file-like or path-like
         buffer to write to
    """
    with TextFileWriter(buf) as f:
        f.write("Hello, world!")

def myfunc_read(buf):
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

# write - with a path-like object
myfunc_write('myfile.txt')

# write - with a file-like object
with open('myfile.txt', 'w') as f:
    myfunc_write(f)

# read - with a path-like object
print(myfunc_read('myfile.txt')

# read - with a file-like object
with open('myfile.txt', 'r') as f:
    print(myfunc_read(f))
```
