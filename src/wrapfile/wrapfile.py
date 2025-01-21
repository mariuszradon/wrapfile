import io
import os

class FileWrapper:
    """File wrapper
    """
    def __init__(self, arg=None, /, mode=None):

        # is arg None, file-like or path-like?
        if arg is None:
            if 'b' in mode:
                self.actual_file = io.BytesIO()
            else:
                self.actual_file = io.StringIO()
            self.should_close = True
        elif hasattr(arg, "fileno"):
            self.actual_file = arg
            self.should_close = False
        else:
            name, ext = os.path.splitext(arg)
            self.actual_file = open(arg, mode)
            self.should_close = True

    def close(self):
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
    def __init__(self, arg, /):
        super().__init__(arg, 'rt')

class TextFileWriter(FileWrapper):
    def __init__(self, arg, /):
        super().__init__(arg, 'wt')

    def getvalue(self):
        if hasattr(self.actual_file, "getvalue"):
            return self.actual_file.getvalue()
        else:
            return None

def wrapfile(arg, /, mode):
    if mode == 'rt':
        return TextFileReader(arg)
    elif mode == 'wt':
        return TextFileWriter(arg)
    else:
        return FileWrapper(arg, mode)

