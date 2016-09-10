from hotikeys.customtypes import IEnum


class KeyState(IEnum):
    Up = 0
    Down = 1


class InputDevice(IEnum):
    none = 0
    Keyboard = 1
    Mouse = 2


class EventId(IEnum):
    WM_KEYDOWN = (0x100, KeyState.Down, InputDevice.Keyboard)
    WM_KEYUP = (0x101, KeyState.Up, InputDevice.Keyboard)
    WM_SYSKEYDOWN = (0x104, KeyState.Down, InputDevice.Keyboard)
    WM_SYSKEYUP = (0x105, KeyState.Up, InputDevice.Keyboard)
    WM_MOUSEMOVE = (0x200, None, InputDevice.Mouse)
    WM_LBUTTONDOWN = (0x201, KeyState.Down, InputDevice.Mouse)
    WM_LBUTTONUP = (0x202, KeyState.Up, InputDevice.Mouse)
    WM_RBUTTONDOWN = (0x204, KeyState.Down, InputDevice.Mouse)
    WM_RBUTTONUP = (0x205, KeyState.Up, InputDevice.Mouse)
    WM_MBUTTONDOWN = (0x207, KeyState.Down, InputDevice.Mouse)
    WM_MBUTTONUP = (0x208, KeyState.Up, InputDevice.Mouse)
    WM_MOUSEWHEEL = (0x20A, None, InputDevice.Mouse)
    WM_XBUTTONDOWN = (0x020B, KeyState.Down, InputDevice.Mouse)
    WM_XBUTTONUP = (0x020C, KeyState.Up, InputDevice.Mouse)
    WM_NCXBUTTONDOWN = (0x00AB, KeyState.Down, InputDevice.Mouse)
    WM_NCXBUTTONUP = (0x00AC, KeyState.Up, InputDevice.Mouse)

    def __new__(cls, code, state, device):
        obj = object.__new__(cls)
        obj._value_ = code  # type: int
        return obj

    def __init__(self, code, state, device):
        self.code = code  # type: int
        self.state = state  # type: KeyState
        self.device = device  # type: InputDevice


class Key(IEnum):
    # A-Z
    A = 0x41
    B = 0x42
    C = 0x43
    D = 0x44
    E = 0x45
    F = 0x46
    G = 0x47
    H = 0x48
    I = 0x49
    J = 0x4A
    K = 0x4B
    L = 0x4C
    M = 0x4D
    N = 0x4E
    O = 0x4F
    P = 0x50
    Q = 0x51
    R = 0x52
    S = 0x53
    T = 0x54
    U = 0x55
    V = 0x56
    W = 0x57
    X = 0x58
    Y = 0x59
    Z = 0x60

    # 0-9
    D0 = 0x30
    D1 = 0x31
    D2 = 0x32
    D3 = 0x33
    D4 = 0x34
    D5 = 0x35
    D6 = 0x36
    D7 = 0x37
    D8 = 0x38
    D9 = 0x39

    # F1-F32
    F1 = 0X70
    F2 = 0X71
    F3 = 0X72
    F4 = 0X73
    F5 = 0X74
    F6 = 0X75
    F7 = 0X76
    F8 = 0X77
    F9 = 0X78
    F10 = 0X79
    F11 = 0X7A
    F12 = 0X7B
    F13 = 0X7C
    F14 = 0X7D
    F15 = 0X7E
    F16 = 0X7F
    F17 = 0X80
    F18 = 0X81
    F19 = 0X82
    F20 = 0X83
    F21 = 0X84
    F22 = 0X85
    F23 = 0X86
    F24 = 0X87
    F25 = 0X88
    F26 = 0X89
    F27 = 0X8A
    F28 = 0X8B
    F29 = 0X8C
    F30 = 0X8D
    F31 = 0X8E
    F32 = 0X8F

    # Mouse
    LButton = 0x01
    RButton = 0x02
    MButton = 0x04
    XButton1 = 0x05
    XButton2 = 0x06

    # Modifiers
    LShift = 0xA0
    RShift = 0xA1
    LControl = 0xA2
    RControl = 0xA3
    LAlt = 0xA4
    RAlt = 0xA5
    LWin = 0x5B
    RWin = 0x5C

    # Numpad
    Numpad0 = 0x60
    Numpad1 = 0x61
    Numpad2 = 0x62
    Numpad3 = 0x63
    Numpad4 = 0x64
    Numpad5 = 0x65
    Numpad6 = 0x66
    Numpad7 = 0x67
    Numpad8 = 0x68
    Numpad9 = 0x69
    NumpadMultiply = 0x6A
    NumpadAdd = 0x6B
    NumpadSeparator = 0x6C
    NumpadSubtract = 0x6D
    NumpadDecimal = 0x6E
    NumpadDivide = 0x6F

    # Special keys
    Back = 0x8
    Tab = 0x9
    Linefeed = 0xA
    Clear = 0xC
    Enter = 0xD
    Pause = 0x13
    Escape = 0x1B
    Space = 0x20
    Pageup = 0x21
    Pagedown = 0x22
    End = 0x23
    Home = 0x24
    Left = 0x25
    Up = 0x26
    Right = 0x27
    Down = 0x28
    Printscreen = 0x2C
    Insert = 0x2D
    Delete = 0x2E

    # Symbols
    Semicolon = 0xBA
    Plus = 0xBB
    Comma = 0xBC
    Minus = 0xBD
    Period = 0xBE
    Question = 0xBF
    Tilde = 0xC0
    OpenBrackets = 0xDB
    Pipe = 0xDC
    CloseBrackets = 0xDD
    Quotes = 0xDE
    Backslash = 0xE2

    # Lock keys
    CapsLock = 0x14
    NumLock = 0x90
    ScrollLock = 0x91

    # No-idea-what-to-call-these keys
    Cancel = 0x3  # Ctrl+Pause
    ShiftKey = 0x10
    ControlKey = 0x11
    AltKey = 0x12

    # I-don't-know-ASCII-mode keys
    HangulMode = 0x15
    JunjaMode = 0x17
    FinalMode = 0x18
    HanjaMode = 0x19
    KanjiMode = 0x19
    ImeConvert = 0x1C
    ImeNonconvert = 0x1D
    ImeAccept = 0x1E
    ImeModechange = 0x1F

    # ??? keys
    Select = 0x29
    Print = 0x2A
    Execute = 0x2B
    Help = 0x2F
    Apps = 0x5D
    Sleep = 0x5F
    Processkey = 0xE5
    Packet = 0xE7
    Attn = 0xF6
    Crsel = 0xF7
    Exsel = 0xF8
    EraseEof = 0xF9
    Play = 0xFA
    Zoom = 0xFB
    Noname = 0xFC
    Pa1 = 0xFD
    Oem8 = 0xDF
    OemClear = 0xFE

    # Look-at-my-fancy-multimedia-keyboard-anno-2000 keys
    BrowserBack = 0xA6
    BrowserForward = 0xA7
    BrowserRefresh = 0xA8
    BrowserStop = 0xA9
    BrowserSearch = 0xAA
    BrowserFavorites = 0xAB
    BrowserHome = 0xAC
    VolumeMute = 0xAD
    VolumeDown = 0xAE
    VolumeUp = 0xAF
    MediaNextTrack = 0xB0
    MediaPreviousTrack = 0xB1
    MediaStop = 0xB2
    MediaPlayPause = 0xB3
    LaunchMail = 0xB4
    SelectMedia = 0xB5
    LaunchApplication1 = 0xB6
    LaunchApplication2 = 0xB7

    # Not actually keys
    none = 0x0
    KeyCode = 0xFFFF
    Shift = 0x10000
    Control = 0x20000
    Alt = 0x40000
    Modifiers = -0x10000
