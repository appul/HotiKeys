# HotiKeys, simple low level key events.

HotiKeys is a library that provides keyboard and mouse events by using low level Windows hooks.

HotiKeys has no dependancies other than Python 3.5+ itself.

## Usage

`Hotkey` is HotiKey's main class and takes the following arguments:
- `handler`: a `callable` (function/method) that _may_ take a single argument for the event args
- `key`(optional): an `Key` or virtual key code (`int`)
- `modifiers`(optional): an `iterable` of keys
- `events`(optional): an `iterable` containing `KeyState`, `EventId` or an `int` that represents the identifier of the event message

`Hotkey` has the following class attributes for configuration;
- `keyboard` (bool, default: True): Hooks keyboard events if True
- `mouse` (bool, default: True): Hooks mouse events if True
- `no_repeat` (bool, default: True): Blocks subsequent key down events when a key is being hold if True
- `purge_delay` (float, default: 10.000): The time in seconds until pressed keys are removed (in case they're not correctly removed during key up events)
- `threaded` (bool, default: True): Whether the hooks should be registered in new threads to prevent blocking the current thread.

_(Note: `keyboard`, `mouse` and `threaded` have to be set before the hooks are placed, which happens when the first instance of the class is made.)_  
_(Note: these are class wide attributes and affect each instance of `Hotkey`. You can subclass and override these attributes if you wish to have separate configurations.)_


## Code Example
```python
import time
from hotikeys import Hotkey, Key, KeyState, newhotkey

def handler(args):
    print(Key[args.vkey], args.event.state)

def on_ctrl_shift_a():
    print('Ctrl-Shift-A pressed!')
    

@newhotkey(Key.LButton)
def lmb_hotkey(args):
    print('Click, click! ({x}, {y}'.format(x=args.x, y=args.y))

Hotkey(handler, events=(KeyState.Down, KeyState.Up))
Hotkey(on_ctrl_shift_a, Key.A, (Key.LControl, Key.LShift))
time.sleep(5)  # Keep running for 5 seconds to prevent immediate exit
```

Another example can be found in [tests/manual_test.py](tests/manual_test.py), which includes an example of a concurrent loop.

## Documentation
**Currently M.I.A.**
Sadly enough the docs were eaten by a vicious bulldog on their journey here. Hopefully a replacement will find their way here... soon™.
