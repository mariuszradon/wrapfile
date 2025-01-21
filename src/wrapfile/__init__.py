"""wrapfile

Create a file-like wrapper based on the actual file or a path to it,
or an internal memory buffer (whose contents can be returned).

The purpose is to simplify coding functions with a
'filepath_or_buffer' argument meaning that what is supplied as the
argument can be a file-like object, str or path object, or even None
(for writing data to an internal memory buffer).
"""

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass

from .wrapfile import FileWrapper, TextFileReader, TextFileWriter, wrapfile
