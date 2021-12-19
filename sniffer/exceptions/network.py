class UnsupportedVersionException(Exception):
    """The specific version of that protocol is not supported."""
    pass


class SLLUnsupportedError(Exception):
    """SLL is not supported."""
    pass
