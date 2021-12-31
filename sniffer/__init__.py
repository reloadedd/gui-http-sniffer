import sys

from .utils import constants
from .utils.funcutils import handle_error

if sys.version_info.minor != 10:
    handle_error(f'Minimum version supported is [i]Python 3.10[/i]. '
                 f'Your current version is [i]Python '
                 f'{sys.version_info.major}.{sys.version_info.minor}[/i]')
    exit(constants.EXIT_SUCCESS)

if sys.argv[0] != '-m':
    # Make the main function available globally to whoever imports the package
    # And don't make it globally when called as a module in order to prevent
    # RuntimeWarning
    from .__main__ import main
