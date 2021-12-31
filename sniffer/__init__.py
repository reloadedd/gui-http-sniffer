import sys

if sys.argv[0] != '-m':
    # Make the main function available globally to whoever imports the package
    # And don't make it globally when called as a module in order to prevent
    # RuntimeWarning
    from .__main__ import main
