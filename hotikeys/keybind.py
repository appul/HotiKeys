import logging
from typing import Callable, Union, Optional
from typing import Iterable

from hotikeys import Hotkey
from hotikeys import Key
from hotikeys import KeyState
from hotikeys.hotkey import EventArgs
from hotikeys.lleventargs import LowLevelKeyboardArgs, LowLevelMouseArgs

log = logging.getLogger(__name__)
EventHandler = Callable[[Union[LowLevelKeyboardArgs, LowLevelMouseArgs]], Optional[bool]]

KeyArg = Union[int, Key]
ModifierArg = Union[KeyArg, Iterable[KeyArg]]


class Keybind(object):
    def __init__(self, key: KeyArg, modifiers: ModifierArg = None, *, hook: bool = False):
        super().__init__()
        self.hotkey = None  # type: Hotkey
        self.value = False  # type: bool
        self.on_press = None  # type: EventHandler
        self.on_release = None  # type: EventHandler
        self._key = None  # type: int
        self._modifiers = None  # type: Iterable[int]

        self.key = key
        self.modifiers = modifiers
        if hook: self.hook()

    def __call__(self, value: bool = None) -> bool:
        if value is not None:
            self.value = value
        return self.value

    def on_event(self, args: EventArgs):
        press = (args.event.state is KeyState.Down)
        handler = self.on_press if press else self.on_release
        handler_result = handler and handler(args)
        self.value = press if handler_result is None else handler_result

    def hook(self):
        self.hotkey = Hotkey(
            handler=self.on_event,
            key=self.key,
            modifiers=self.modifiers,
            events=(KeyState.Down, KeyState.Up))

    @property
    def key(self) -> int:
        if self.hotkey is not None:
            return self.hotkey.key
        return self._key

    @key.setter
    def key(self, value):
        if self.hotkey is not None:
            self.hotkey.key = value
        self._key = value

    @property
    def modifiers(self) -> Iterable[int]:
        if self.hotkey is not None:
            return self.hotkey.modifiers
        return self._modifiers

    @modifiers.setter
    def modifiers(self, value):
        if self.hotkey is not None:
            self.hotkey.modifiers = value
        self._modifiers = value


class Keytoggle(Keybind):
    def on_event(self, args: EventArgs):
        if args.event.state is KeyState.Down:
            result = self.on_press and self.on_press(args)
            if result is not False:
                self.value = not self.value
