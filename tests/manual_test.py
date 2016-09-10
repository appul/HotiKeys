import asyncio

from hotikeys import Hotkey
from hotikeys.enums import Key
from hotikeys.hotkey import EventProcs


def automated_test(loop):
    def key_handler(proc: EventProcs):
        print(Key[proc.vkey], proc.event, proc.flags)

    def stop_loop():
        print('stopping')
        loop.stop()

    Hotkey(key_handler, None, (), ())
    Hotkey(stop_loop, Key.C, Key.LControl)

    loop.create_task(heartbeat(loop, 0))
    loop.run_forever()


async def heartbeat(loop, count):
    if count > 5:
        return loop.stop()
    await asyncio.sleep(1)
    loop.create_task(heartbeat(loop, count + 1))


# Super automated test. Just eh... hit a few keys and observe console.
# Ctrl-C to stop, if it works.
if __name__ == '__main__':
    automated_test(asyncio.get_event_loop())
