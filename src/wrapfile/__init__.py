from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass

from .wrapfile import FileWrapper, TextFileReader, TextFileWriter, wrapfile
