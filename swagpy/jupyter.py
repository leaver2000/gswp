"""extension for working with jupyter notebooks"""
from IPython.terminal.interactiveshell import TerminalInteractiveShell


def load_ipython_extension(ipython: TerminalInteractiveShell) -> None:
    import nest_asyncio
    import jupyter_black

    nest_asyncio.apply()
    jupyter_black.load_ipython_extension(ipython)


def unload_ipython_extension(ipython: TerminalInteractiveShell) -> None:
    ...
