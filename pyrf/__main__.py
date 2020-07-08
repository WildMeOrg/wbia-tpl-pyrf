# -*- coding: utf-8 -*-
def main():  # nocover
    import pyrf

    print('Looks like the imports worked')
    print('pyrf = {!r}'.format(pyrf))
    print('pyrf.__file__ = {!r}'.format(pyrf.__file__))
    print('pyrf.__version__ = {!r}'.format(pyrf.__version__))
    print('pyrf.RF_CLIB = {!r}'.format(pyrf.RF_CLIB))


if __name__ == '__main__':
    """
    CommandLine:
       python -m pyrf
    """
    main()
