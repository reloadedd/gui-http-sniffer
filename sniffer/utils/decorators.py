import os
import platform
from functools import wraps
from collections.abc import Callable
from .constants import ROOT_EUID
from .funcutils import handle_error


def require_root(func: Callable[..., None]) -> Callable[..., None]:
    """Require that the user has root permissions before calling.

    The user that ran the program must have root access before invoking the
    function.

    Parameters
    ----------
    func : Callable[..., None]
        The function to be called

    Returns
    -------
    Callable[..., None]
        The function being decorated
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == 'Windows':
            handle_error('Unfortunately, sniffing is not supported on Windows')

        # Check if the current user is root
        if os.geteuid() != ROOT_EUID:
            handle_error('You need [i]root[/i] privileges in order to use raw '
                         'sockets')

        # Now, after doing the checks, call the actual function
        func(*args, **kwargs)

    return wrapper
