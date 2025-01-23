import io
import os
from .error import WrapFileValueError

class FileWrapper:
    """File wrapper
    """
    def __init__(self, filepath_or_buffer, /, mode='w'):
        """Construct file wrapper based on filepath or buffer

        Parameters:
        -----------
        filepath_or_buffer: str, path or file-like object
             actual file or a path to it.
             If the path is provided, the actual file will opened
             using open() or gzip.open() if the path endswith '.gz',
             or bz2.open() if the path endswith '.bz2'.
             For the special value None, an in-memory buffer will be
             opened, to which the data can be written.
             Depending on the value of mode, this in-memory buffer 
             will be io.StringIO (mode in ['w', 'wt'])
             or io.BytesIO (mode == 'wb').

        mode : str, optional
             the mode in which the file will be opened if needed
             using open(). If default to 'w'.
             If the argument is a file-like object, the argument
             mode is ignored; in particular, there is no check
             if the file has been opened in the appropriate mode.
        """
        # is filepath_or_buffer None, file-like or path-like?
        if filepath_or_buffer is None:
            if mode == 'wb':
                self.actual_file = io.BytesIO()
            elif mode in ['w', 'wt']:
                self.actual_file = io.StringIO()
            else:
                raise WrapFileValueError(
                    f"Invalid mode for an in-memory buffer: '{mode}'"
                )
            self.should_close = True
        elif hasattr(filepath_or_buffer, "fileno"):
            self.actual_file = filepath_or_buffer
            self.should_close = False
        else:
            name, ext = os.path.splitext(filepath_or_buffer)
            if ext == '.gz':
                import gzip
                self.actual_file = gzip.open(
                    filepath_or_buffer, mode
                )
            elif ext == '.bz2':
                import bz2
                self.actual_file = bz2.open(
                    filepath_or_buffer, mode
                )
            else:
                self.actual_file = open(filepath_or_buffer, mode)
            self.should_close = True

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.actual_file)})'

    def close(self):
        """Close the file

        The actual file is only closed in it was opened
        when constructing the wrapper.
        """
        if self.should_close:
            return self.actual_file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
        return False

    def __iter__(self):
        return self.actual_file

    def __next__(self):
        return next(self.actual_file)

    def __getattr__(self, name):
        return getattr(self.actual_file, name)

class TextFileReader(FileWrapper):
    def __init__(self, filepath_or_buffer, /):
        super().__init__(filepath_or_buffer, 'rt')

class TextFileWriter(FileWrapper):
    def __init__(self, filepath_or_buffer, /):
        super().__init__(filepath_or_buffer, 'wt')

    def getvalue(self):
        """Contents written to the in-memory buffer or None

        Returns:
        --------
        str or None:
            contents written to the in-memory buffer
            or None if no in-memory buffer has been created
            by this instance.
        """
        if hasattr(self.actual_file, "getvalue"):
            return self.actual_file.getvalue()
        else:
            return None

def wrapfile(filepath_or_buffer, /, mode):
    if mode in ['r', 'rt']:
        return TextFileReader(filepath_or_buffer)
    elif mode in ['w', 'rw']:
        return TextFileWriter(filepath_or_buffer)
    else:
        return FileWrapper(filepath_or_buffer, mode)

