from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Union

from hotikeys import Hotkey
from hotikeys import KeyState
from hotikeys.lleventargs import LowLevelKeyboardArgs
from hotikeys.lleventargs import LowLevelMouseArgs

EventHandler = Callable[[Union[LowLevelKeyboardArgs, LowLevelMouseArgs]], Optional[bool]]


class KeybindProperty(property):
    def __init__(self, key, modifiers=None, *, hook=False):
        super().__init__()
        self.value = False  # type: bool
        self.hotkey = None  # type: Hotkey
        self.on_press = None  # type: EventHandler
        self.on_release = None  # type: EventHandler
        self._key = None  # type: int
        self._modifiers = None  # type: Iterable[int]

        self.key = key
        self.modifiers = modifiers
        if hook: self.hook()

    def __call__(self, handler):
        return self.presser(handler)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        if self.fget is not None:
            return self.fget(instance)
        return self.value

    def __set__(self, instance, value):
        if self.fset is not None:
            self.fset(instance, value)
        self.value = value

    def on_event(self, args):
        press = (args.event.state is KeyState.Down)
        handler = self.on_press if press else self.on_release
        value = handler and handler(args)
        self.value = press if value is None else value

    def hook(self):
        self.hotkey = Hotkey(
            handler=self.on_event,
            key=self.key,
            modifiers=self.modifiers,
            events=(KeyState.Down, KeyState.Up))

    def presser(self, handler):
        self.on_press = handler
        return self

    def releaser(self, handler):
        self.on_release = handler
        return self

    @property
    def key(self) -> int:
        if self.hotkey is not None:
            return self.hotkey.key
        return self._key

    @key.setter
    def key(self, key):
        if self.hotkey is not None:
            self.hotkey.key = key
        self._key = key

    @property
    def modifiers(self) -> Iterable[int]:
        if self.hotkey is not None:
            return self.hotkey.modifiers
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        if self.hotkey is not None:
            self.hotkey.modifiers = modifiers
        self._modifiers = modifiers

    def getter(self, fget):
        raise NotImplemented('{cls}.getter is disabled as its behavior has '
                             'been overridden, use {cls}.getterf instead.'
                             .format(cls=self.__class__.__name__))

    def getterf(self, fget):
        """Note: This does not return a copy of the property to prevent copies of the hotkey hooks"""
        self.fget = fget
        return self

    def setter(self, fset):
        raise NotImplemented('{cls}.setter is disabled as its behavior has '
                             'been overridden, use {cls}.setterf instead.'
                             .format(cls=self.__class__.__name__))

    def setterf(self, fset):
        """Note: This does not return a copy of the property to prevent copies of the hotkey hooks"""
        self.fset = fset
        return self

    def deleter(self, fdel):
        raise NotImplemented('{cls}.deleter is disabled as its behavior has '
                             'been overridden, use {cls}.deleterf instead.'
                             .format(cls=self.__class__.__name__))

    def deleterf(self, fdel):
        """Note: This does not return a copy of the property to prevent copies of the hotkey hooks"""
        self.fdel = fdel
        return self


class KeytoggleProperty(KeybindProperty):
    def on_event(self, args):
        if args.event.state is KeyState.Down:
            result = self.on_press and self.on_press(args)
            if result is not False:
                self.value = not self.value
