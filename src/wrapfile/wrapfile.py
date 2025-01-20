import io

class FileWrapper:
    """File wrapper
    """
    def __init__(self, arg=None, /, mode=None):

        # is arg None, file-like or path-like?
        if arg is None:
            self.actual_file = io.StringIO()
            self.should_close = True
            self.has_value = True
        elif hasattr(arg, "fileno"):
            self.actual_file = arg
            self.should_close = False
            self.has_value = False
        else:
            self.actual_file = open(arg, mode)
            self.should_close = True
            self.has_value = False

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
        super().__init__(arg, 'r')

class TextFileWriter(FileWrapper):
    def __init__(self, arg=None, /):
        super().__init__(arg, 'w')

def wrapfile(arg, /, mode):
    return FileWrapper(arg, mode)

