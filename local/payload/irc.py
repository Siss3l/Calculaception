"""
This module provides methods to work with Windows 10 Calculator 64-bit.
"""

from __future__ import print_function

from dataclasses import dataclass
from functools import partial
from glob import glob
from locale import getdefaultlocale
from pathlib import Path
from shutil import rmtree
from subprocess import Popen
from sys import exit as close, modules
from tempfile import gettempdir
from time import time
from typing import Callable, Union

from frida import get_local_device, kill, InvalidArgumentError, InvalidOperationError, \
    NotSupportedError, ProcessNotFoundError, ProcessNotRespondingError, TransportError
from loguru import logger
from psutil import process_iter, AccessDenied, NoSuchProcess, ZombieProcess
from rich import print as show
from yaml import safe_load

calculator, calc = "Calculator.exe", "calc.exe"
ex = r"explorer.exe shell:AppsFolder\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
hook = (Path(__file__).parent / "hook.jsx").read_text()
lang = safe_load((Path(__file__).parent / "i18n.yml").read_bytes())["languages"].get(
    getdefaultlocale()[False].split("_")[0], {"btn": "Send feedback", "abt": "About"})


def checking() -> bool:
    """
    Checks if Calculator process exists and runs in foreground.
    .. note::
        A new instance of Explorer.exe or ApplicationFrameHost.exe can be started
        in the background before a reboot and can potentially provoke deadlocks.
    :rtype: bool
    """
    for proc in process_iter(attrs=["name", "username"]):
        try:
            if proc.name().casefold() in (calculator.casefold(), calc.casefold()):
                if proc.status() == "running":  # Might not be visible sometimes.
                    show(f"[bold cyan]Process { {proc} } found[/bold cyan] :thumbs_up:")
                    return True
                if proc.status() == "stopped":
                    (*_,) = proc.terminate(), proc.wait()
                    break  # This is not useful with "for-else".
        except (AccessDenied, NoSuchProcess, ZombieProcess):
            pass
    _ex = pop(ex)
    if _ex:
        return _ex
    _calc = pop(calc)
    if _calc:
        return _calc
    return False


def clean():
    """
    Removes Frida's temporary folders (except if used) who needs several
    Dynamic Link Libraries to work that can take up some space.
    """
    _ = [rmtree(f, ignore_errors=True, onerror=None) for f in glob(f"{gettempdir()}/frida-*")]


def pop(value: Union[str, int]) -> bool:
    """
    Try to run Calculator along different ways with a minute timeout.
    .. note::
        There may be a false positive if notably OpenWith.exe (of returncode belonging to the N set)
        is also running or that Explorer.exe is launched without succeeding in finding Calculator.
    :rtype: nonlocal bool
    """
    try:
        with Popen(value) as _p:
            _m = time() + 60
            poll = _p.poll()
            while poll is None:
                poll = _p.poll()
                if time() > _m:
                    (*_,) = _p.terminate(), _p.wait()
                    return False
    except FileNotFoundError:
        return False
    return True


@dataclass
class Hooking:
    """
    Class that allows to interact with Calculator.
    """

    def __init__(self, process: Union[str, int],
                 _on_send_callback: Callable[[str, int, bytes], None] = None,
                 _on_recv_callback: Callable[[str, int, bytes], None] = None):
        self.local_device = get_local_device()
        self.process_id = self.local_device.get_process(process).pid
        self.session = self.local_device.attach(self.process_id)
        self.script = self.session.create_script(hook, runtime="v8")
        self.script.on("message", self._on_message)
        self.script.load()
        show(f'[bold cyan]Please click on the \"'
             f'[italic green]{lang["btn"]}[/italic green]\" button in '
             f'the \"[italic bold green]{lang["abt"]}[/italic bold green]\" section.[/bold cyan]'
             )
        input("Press <Enter> key to close.\n")
        self.script.unload()
        self.session.detach()
        kill(self.process_id)
        clean()
        close()

    @staticmethod
    def _on_message(message, data):
        try:
            if data is not None:
                show(f"[bold red]{data}[/bold red]")
            show(f"[bold magenta]{message['payload']}[/bold magenta]")
        except ImportError as error:
            logger.exception(f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    logger.info("If libraries have not been imported it cannot be a routine supported here.")
    if {"frida", "loguru", "psutil", "rich", "yaml"}.issubset(modules):
        if checking():
            try:
                _ = partial(Hooking)(calculator)
            except (InvalidArgumentError, InvalidOperationError, NotSupportedError,
                    ProcessNotFoundError, ProcessNotRespondingError, TransportError) as e:
                logger.exception(f"{type(e).__name__}: {e}")
                clean()
