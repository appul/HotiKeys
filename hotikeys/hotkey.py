from inspect import signature
from typing import Callable, Iterable
from typing import Union

from hotikeys.core import HotkeyCore
from hotikeys.enums import KeyState, Key, EventIdentifier
from hotikeys.lleventargs import LowLevelKeyboardArgs, LowLevelMouseArgs

EventArgs = Union[LowLevelKeyboardArgs, LowLevelMouseArgs]
_HandlerArg = Callable[[EventArgs], None]
_KeyArg = Union[int, Key]
_EventArg = Union[int, EventIdentifier, KeyState]


class Hotkey(HotkeyCore):
    def __init__(self,
                 handler: _HandlerArg,
                 key: _KeyArg = None,
                 modifiers: Union[_KeyArg, Iterable[_KeyArg], None] = None,
                 events: Union[_EventArg, Iterable[_EventArg], None] = KeyState.Down):
        self._handler = None  # type: _HandlerArg
        self._key = None  # type:
        self._modifiers = None  # type: Iterable[int]
        self._events = None  # type: Iterable[int]
        self._handler_takes_args = None  # type: bool

        self.handler = handler
        self.key = key
        self.modifiers = modifiers
        self.events = events

    def on_event(self, args):
        if not isinstance(args, (LowLevelKeyboardArgs, LowLevelMouseArgs)):
            raise TypeError('expected (LowLevelKeyboardArgs, LowLevelMouseArgs)'
                            ' for args, got {0}'.format(type(args)))

        if not self._match_key(args): return
        if not self._match_modifiers(): return
        if not self._match_events(args): return
        if self._handler_takes_args:
            self.handler(args)
        else:
            self.handler()

    def on_mouse(self, args):
        if not self._match_events(args, False): return
        self.handler(args)

    def _match_key(self, args, implicit=True) -> bool:
        if self.key is None and implicit: return True
        return self.key == args.vkey

    def _match_modifiers(self, implicit=True) -> bool:
        if not self.modifiers and implicit: return True
        return all(self.is_pressed(key) for key in self.modifiers)

    def _match_events(self, args, implicit=True) -> bool:
        if not self.events and implicit: return True
        if args.event is None: return False
        if int(args.event) in self.events: return True
        if args.event.state is None: return False
        if int(args.event.state) in self.events: return True
        return False

    @property
    def handler(self) -> _HandlerArg:
        return self._handler

    @handler.setter
    def handler(self, handler):
        if not callable(handler):
            raise TypeError('expected callable for handler, received: {0}'.format(type(handler)))
        self._handler_takes_args = bool(len(signature(handler).parameters))
        self._handler = handler

    @property
    def key(self) -> int:
        return self._key

    @key.setter
    def key(self, key):
        if key is not None:
            self._key = int(key)
        else:
            self._key = None

    @property
    def modifiers(self) -> Iterable[int]:
        return self._modifiers

    @modifiers.setter
    def modifiers(self, modifiers):
        if modifiers is not None:
            if isinstance(modifiers, (int, Key)):
                modifiers = (modifiers,)
            if not isinstance(modifiers, (list, tuple)):
                raise TypeError('expected Key, int, list or tuple'
                                ' for modifiers, received: {0}'.format(type(modifiers)))
            self._modifiers = tuple(int(modifier) for modifier in modifiers)
        else:
            self._modifiers = ()

    @property
    def events(self) -> Iterable[int]:
        return self._events

    @events.setter
    def events(self, events):
        if events is not None:
            if isinstance(events, (int, EventIdentifier, KeyState)):
                events = (events,)
            if not isinstance(events, (list, tuple)):
                raise TypeError('expected EventIdentifier, KeyState, int, list or tuple'
                                ' for events, received: {0}'.format(type(events)))
            self._events = tuple(int(event) for event in events)
        else:
            self._events = None
