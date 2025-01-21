class WrapFileException(Exception):
    """Exception related to wrapfile"""

class WrapFileValueError(WrapFileException, ValueError):
    """ValueError related to wrapfile"""
