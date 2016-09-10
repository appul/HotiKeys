import time
from _ctypes import POINTER
from abc import abstractmethod
from ctypes import c_int, c_void_p
from typing import Dict
from typing import List

from hotikeys.enums import KeyState, EventId
from hotikeys.lleventargs import LowLevelKeyboardArgs, LowLevelMouseArgs
from hotikeys.windowshook import WindowsHook

_WH_KEYBOARD_LL = 0x0D
_WH_MOUSE_LL = 0x0E


class HotkeyCoreMeta(type):
    def __init__(cls, name, bases=None, variables=None):
        super().__init__(name, bases, variables)
        for base in bases:
            for k, v in vars(base).items():
                if isinstance(v, (list, dict)):
                    new = type(v)()
                    setattr(cls, k, new)


class HotkeyCore(metaclass=HotkeyCoreMeta):
    purge_delay = 10.000
    threaded = True
    no_repeat = True
    keyboard = True
    mouse = True

    _pressed = {}  # type: Dict[int, float]

    __hooked = False
    __hotkeys = []  # type: List[HotkeyCore]
    __last_key = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        cls.__hotkeys.append(obj)
        if not cls.__hooked:
            cls.__hooked = True
            cls.__install_hooks()
        return obj

    @classmethod
    def __install_hooks(cls):
        signature = c_int, c_int, POINTER(c_void_p)

        if cls.keyboard:
            keyboard_hook = WindowsHook(_WH_KEYBOARD_LL, signature, cls.__on_keyboard)
            keyboard_hook.register(cls.threaded)

        if cls.mouse:
            mouse_hook = WindowsHook(_WH_MOUSE_LL, signature, cls.__on_mouse)
            mouse_hook.register(cls.threaded)

    @classmethod
    def __on_keyboard(cls, ncode, wparam, lparam):
        cls.__on_event(LowLevelKeyboardArgs(ncode, wparam, lparam))

    @classmethod
    def __on_mouse(cls, ncode, wparam, lparam):
        cls.__on_event(LowLevelMouseArgs(ncode, wparam, lparam))

    @classmethod
    def __on_event(cls, args):
        if args.event is EventId.WM_MOUSEMOVE or args.event is EventId.WM_MOUSEWHEEL:
            for hotkey in cls.__hotkeys:
                hotkey.on_mouse(args)
            return

        cls.__purge_keys()
        cls.__set_key_state(args)
        if not cls.__prevent_repeat(args):
            for hotkey in cls.__hotkeys:
                hotkey.on_event(args)

    @classmethod
    def __purge_keys(cls):
        now = time.time()
        for key, purge_time in list(cls._pressed.items()):
            if purge_time < now:
                cls._pressed.pop(key)

    @classmethod
    def __set_key_state(cls, args):
        if args.event.state == KeyState.Down:
            cls._pressed[args.vkey] = time.time() + cls.purge_delay
        elif args.vkey in cls._pressed:
            cls._pressed.pop(args.vkey)

    @classmethod
    def __prevent_repeat(cls, args):
        if not cls.no_repeat:
            return False
        if args.event.state == KeyState.Up:
            cls.__last_key = None
            return False
        if args.vkey == cls.__last_key:
            return True
        cls.__last_key = args.vkey

    @classmethod
    def is_pressed(cls, key) -> bool:
        return int(key) in cls._pressed

    @abstractmethod
    def on_event(self, args):
        pass

    @abstractmethod
    def on_mouse(self, args):
        pass
