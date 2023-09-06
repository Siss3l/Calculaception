# pylint: disable=line-too-long, invalid-name
"""
This module provides methods to work with Windows 10 Calculator 64-bit.
"""

from dataclasses import dataclass
from functools import partial
from glob import glob
from json import loads
from locale import getlocale
from pathlib import Path
from shutil import rmtree
from subprocess import Popen
from sys import exit as down, modules
from tempfile import gettempdir
from time import time
from typing import Callable, NoReturn, Union

from frida import get_local_device, kill, InvalidArgumentError, InvalidOperationError, NotSupportedError, ProcessNotFoundError, ProcessNotRespondingError, TransportError
from loguru import logger
from psutil import process_iter, AccessDenied, NoSuchProcess, ZombieProcess
from rich import print as show


def checking() -> bool:
    """
    Checking if Calculator/CalculatorApp process exists and runs in foreground.
    .. note::
        A new instance of Explorer.exe or ApplicationFrameHost.exe can be started
        in the background before a reboot and can potentially provoke deadlocks.
    :rtype: bool
    """
    for proc in process_iter(attrs=["name", "username"]):
        try:
            if proc.name().casefold() in ("calculator.exe", "calculatorapp.exe", "calc.exe"):
                if proc.status() == "running":
                    show(f"[bold cyan]Process { {proc} } found[/bold cyan] :thumbs_up:")
                    return True
                if proc.status() == "stopped":
                    (*_,) = proc.terminate(), proc.wait()
                    break
        except (AccessDenied, NoSuchProcess, ZombieProcess):
            pass
    return bool(pop(r"explorer.exe shell:AppsFolder\Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"))


def pop(value: Union[str, int]) -> bool:
    """
    Try to run Calculator with a minute timeout.
    .. note::
        There may be false positive possibly if *OpenWith.exe* (of returncode belonging to the N set)
        is running or that *Explorer.exe* is launched without finding Calculator process.
    :rtype: bool
    """
    try:
        with Popen(value) as p:
            m = time() + 60
            poll = p.poll()
            while poll is None:
                poll = p.poll()
                if time() > m:
                    (*_,) = p.terminate(), p.wait()
                    return False
    except FileNotFoundError:
        return False
    return True


@dataclass
class Hooking:
    """
    Class that allows to interact with Calculator process with Frida.
    """

    def __init__(self, process: Union[str, int], _on_send_callback: Callable[[str, int, bytes], None] = None, _on_recv_callback: Callable[[str, int, bytes], None] = None):
        lng = list(list(({k: v for k, v in loads((Path(__file__).parent / "i18n.json").read_bytes()).items() if (getlocale()[0].split("_")[0].casefold() or "en")
                          in k.casefold() } or {"en": {"btn": "Send feedback", "abt": "About"}}).values())[0].values())
        self.local_device = get_local_device()
        self.process_id = self.local_device.get_process(process).pid
        self.session = self.local_device.attach(self.process_id)
        self.script = self.session.create_script((Path(__file__).parent / "hook.jsx").read_text(), runtime="v8")
        self.script.on("message", self._on_message)
        self.script.load()
        show(f'[bold cyan]Please click on the \"[italic green]{lng[0]}[/italic green]\" button in the \"[italic bold green]{lng[1]}[/italic bold green]\" section.[/bold cyan]')
        input("Please press the <Enter> keyboard key to quit.\n")
        self.script.unload()
        self.session.detach()
        kill(self.process_id)
        _ = [rmtree(f, ignore_errors=1, onerror=None) for f in glob(f"{gettempdir()}/frida-*")]
        down()

    @staticmethod
    def _on_message(message: Union[dict, str], data: Union[dict, str]) -> NoReturn:
        try:
            if data is not None:
                show(f"[bold red]{data}[/bold red]")
            show(f"[bold magenta]{message['payload']}[/bold magenta]")
        except ImportError as error:
            logger.exception(f"{type(error).__name__}: {error}.")


if __name__ == "__main__":
    logger.info("If libraries have not been imported it cannot be a routine supported here.")
    if {"frida", "loguru", "psutil", "rich"}.issubset(modules):
        if checking():
            try:
                _ = partial(Hooking)("calculator.exe")
            except ProcessNotFoundError:
                try:
                    _ = partial(Hooking)("calculatorapp.exe")
                except ProcessNotFoundError:
                    try:
                        _ = partial(Hooking)("calc.exe")
                    except ProcessNotFoundError:
                        _ = partial(Hooking)("calculator.exe")
            except (InvalidArgumentError, InvalidOperationError, NotSupportedError, ProcessNotFoundError, ProcessNotRespondingError, TransportError) as e:
                logger.exception(f"{type(e).__name__}: {e}.")
            finally:
                _ = [rmtree(f, ignore_errors=1, onerror=None) for f in glob(f"{gettempdir()}/frida-*")]
                down()
