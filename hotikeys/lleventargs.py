from typing import Any
from typing import Tuple

from hotikeys.customtypes import FlagsDword
from hotikeys.enums import EventIdentifier


class LowLevelEventArgs(object):
    def __init__(self, ncode, wparam, lparam):
        self.ncode = ncode  # type: int
        self.wparam = wparam  # type: int
        self.lparam = lparam  # type: Tuple[Any]

        self.event = EventIdentifier[wparam]  # type: EventIdentifier


class LowLevelKeyboardArgs(LowLevelEventArgs):
    def __init__(self, ncode, wparam, lparam):
        super().__init__(ncode, wparam, lparam)

        self.vkey = 0xFFFF & lparam[0]  # type: int
        self.scan_code = lparam[1]  # type: int
        self.flags = LowLevelKeyboardFlags(lparam[2] or 0)  # type: LowLevelKeyboardFlags
        self.time = lparam[3]  # type: int


class LowLevelKeyboardFlags(FlagsDword):
    @property
    def extended(self):
        return self[0]

    @property
    def lower_il_injected(self):
        return self[1]

    @property
    def injected(self):
        return self[4]

    @property
    def altdown(self):
        return self[5]

    @property
    def up(self):
        return self[7]


class LowLevelMouseArgs(LowLevelEventArgs):
    def __init__(self, ncode, wparam, lparam):
        super().__init__(ncode, wparam, lparam)
        self.x = lparam[0]  # type: int
        self.y = lparam[1]  # type: int
        self.mouse_data = lparam[2]  # type: int
        self.flags = LowLevelMouseFlags(lparam[3] or 0)  # type: LowLevelMouseFlags
        self.time = lparam[4]  # type: int

        # Since it's constant, a property would be an unnecessary expense.
        self.vkey = self.get_vkey(wparam, lparam)  # type: int

    @property
    def point(self):
        return self.x, self.y

    @classmethod
    def get_vkey(cls, wparam, lparam) -> int:
        vkey = cls.wparam_to_vkeys[wparam & 0xF]
        if vkey is 0x0:
            return 0x4 + lparam[2]
        return vkey

    wparam_to_vkeys = (
        None,  # (0x200) WM_MOUSEMOVE
        0x1,  # (0x201) WM_LBUTTONDOWN
        0x1,  # (0x202) WM_LBUTTONUP
        0x1,  # (0x203) WM_LBUTTONDBLCLK
        0x2,  # (0x204) WM_RBUTTONDOWN
        0x2,  # (0x205) WM_RBUTTONUP
        0x2,  # (0x206) WM_RBUTTONDBLCLK
        0x4,  # (0x207) WM_MBUTTONDOWN
        0x4,  # (0x208) WM_MBUTTONUP
        0x4,  # (0x209) WM_MBUTTONDBLCLK
        None,  # (0x20A) WM_MOUSEWHEEL
        0x0,  # (0x20B, 0x0AB) WM_XBUTTONDOWN, WM_NCXBUTTONDOWN
        0x0,  # (0x20C, 0x0AC) WM_XBUTTONUP, WM_NCXBUTTONUP
        0x0,  # (0x20D, 0x0AD) WM_XBUTTONDBLCLK, WM_NCXBUTTONDBLCLK
    )


class LowLevelMouseFlags(FlagsDword):
    @property
    def injected(self):
        return self[0]

    @property
    def lower_il_injected(self):
        return self[1]
