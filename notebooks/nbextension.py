"""extension for working with jupyter notebooks"""
import os
from IPython.terminal.interactiveshell import TerminalInteractiveShell

def getenv():
    jupenv = os.getenv("JUPYTER_ENV")
    gswp = f'{os.environ["HOME"]}/gswp'
    if jupenv:
        return f"{jupenv}:{gswp}"
    return gswp

    
JUPYTER_ENV = getenv()

def load_ipython_extension(ipython: TerminalInteractiveShell) -> None:
    os.environ["JUPYTER_ENV"] = JUPYTER_ENV
    import nest_asyncio
    import jupyter_black

    nest_asyncio.apply()
    jupyter_black.load_ipython_extension(ipython)


def unload_ipython_extension(ipython: TerminalInteractiveShell) -> None:
    ...