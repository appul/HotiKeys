import atexit
import ctypes
import logging
import sys
import threading
from _ctypes import byref
from ctypes import wintypes
from traceback import print_exception
from typing import Any
from typing import Callable
from typing import List

log = logging.getLogger(__name__)

_win32_GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
_win32_SetWindowsHookExA = ctypes.windll.user32.SetWindowsHookExA
_win32_UnhookWindowsHookEx = ctypes.windll.user32.UnhookWindowsHookEx
_win32_CallNextHookEx = ctypes.windll.user32.CallNextHookEx
_win32_PeekMessageW = ctypes.windll.user32.PeekMessageW
_win32_GetMessageW = ctypes.windll.user32.GetMessageW
_win32_TranslateMessage = ctypes.windll.user32.TranslateMessage
_win32_DispatchMessageW = ctypes.windll.user32.DispatchMessageW


class WindowsHook(object):
    def __init__(self, event, signature, handler, *, polling=False):
        self.event = event  # type: int
        self.signature = signature  # type: List[Any]
        self.handler = handler  # type: Callable[[Any], Any]
        self.hook_id = None  # type: int
        self.polling = polling

    def hook(self):
        def on_event(*args, **kwargs):
            # noinspection PyBroadException
            try:
                self.handler(*args, **kwargs)
            except:
                print_exception(*sys.exc_info())
            finally:
                return _win32_CallNextHookEx(None, *args, **kwargs)

        func = ctypes.CFUNCTYPE(ctypes.c_int, *self.signature)
        pntr = func(on_event)
        hmod = _win32_GetModuleHandleA(None)
        self.hook_id = _win32_SetWindowsHookExA(self.event, pntr, hmod, 0)
        atexit.register(self.unhook)

        msg = wintypes.MSG()
        while self.hook_id:
            if self.polling:
                _win32_PeekMessageW(None, 0, 0, 0, 0)
            else:
                _win32_GetMessageW(byref(msg), 0, 0, 0)
                _win32_TranslateMessage(byref(msg))
                _win32_DispatchMessageW(byref(msg))

    def unhook(self):
        _win32_UnhookWindowsHookEx(self.hook_id)
        self.hook_id = None

    def register(self, threaded=True):
        if threaded:
            thread = threading.Thread(target=self.hook)
            thread.setDaemon(True)
            thread.start()
        else:
            self.hook()


def windowshookmethod(event, signature, threaded=True):
    def decorator(method):
        hook = WindowsHook(event, signature, method)
        hook.register(threaded)
        return method

    return decorator
