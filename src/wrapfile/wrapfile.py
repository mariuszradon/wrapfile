class FileWrapper:
    """File wrapper
    """
    def __init__(self, arg, /, mode):

        # is arg file-like or path-like?
        if hasattr(arg, "fileno"):
            self.actual_file = arg
            self.should_close = False
        else:
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
        super().__init__(arg, 'r')

class TextFileWriter(FileWrapper):
    def __init__(self, arg, /):
        super().__init__(arg, 'w')

def wrapfile(arg, /, mode):
    return FileWrapper(arg, mode)

