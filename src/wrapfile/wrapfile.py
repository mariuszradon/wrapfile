import io
import os

class FileWrapper:
    """File wrapper
    """
    def __init__(self, filepath_or_buffer, /, mode='r'):
        """Construct file wrapper based on filepath or buffer

        Parameters:
        -----------
        filepath_or_buffer: str, path or file-like object
             actual file or a path to it.
             For the special value None, a memory buffer will be
             opened, to which the data can be written.
             This memory buffer will be io.StringIO or io.BytesIO,
             depending on the value of mode.

        mode : str, optional
             the mode in which the file will be opened if needed
             using open(). If default to 'r'.
             If the argument is a file-like object, the argument
             mode is not used; in particular there is no check
             if the file is open in the appropriate mode.
        """
        # is filepath_or_buffer None, file-like or path-like?
        if filepath_or_buffer is None:
            if 'b' in mode:
                self.actual_file = io.BytesIO()
            else:
                self.actual_file = io.StringIO()
            self.should_close = True
        elif hasattr(filepath_or_buffer, "fileno"):
            self.actual_file = filepath_or_buffer
            self.should_close = False
        else:
            name, ext = os.path.splitext(filepath_or_buffer)
            self.actual_file = open(filepath_or_buffer, mode)
            self.should_close = True

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
    
    def __getattr__(self, name):
        return getattr(self.actual_file, name)

class TextFileReader(FileWrapper):
    def __init__(self, filepath_or_buffer, /):
        super().__init__(filepath_or_buffer, 'rt')

class TextFileWriter(FileWrapper):
    def __init__(self, filepath_or_buffer, /):
        super().__init__(filepath_or_buffer, 'wt')

    def getvalue(self):
        """Contents written to the memory buffer or None

        Returns:
        --------
        str or None:
            contents written to the memory buffer
            or None if there was no memory buffer.
        """
        if hasattr(self.actual_file, "getvalue"):
            return self.actual_file.getvalue()
        else:
            return None

def wrapfile(filepath_or_buffer, /, mode):
    if mode == 'rt':
        return TextFileReader(filepath_or_buffer)
    elif mode == 'rw':
        return TextFileWriter(filepath_or_buffer)
    else:
        return FileWrapper(filepath_or_buffer, mode)

