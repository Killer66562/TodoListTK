from enum import Enum, auto


DB_URL="sqlite:///database.sqlite3"
class FrameType(Enum):
    INDEX = auto()
    TODAY = auto()
    PREVIEW = auto()


class EventType(Enum):
    FONT_CHANGED = auto()
    FS_CHANGED = auto()

    INDEX_BTN_CLICKED = auto()
    TODAY_BTN_CLICKED = auto()
    PREVIEW_BTN_CLICKED = auto()
    CALANDER_BTN_CLICKED = auto()
    SETTINGS_BTN_CLICKED = auto()
    TAG_ADD_BTN_CLICKED = auto()

    MY_ITEMS_BTN_CLICKED = auto()

    INPUT_ROW_BTN_CLICKED = auto()

    COLOR_MODE_CHANGED = auto()