from enum import Enum, auto


DB_URL="sqlite:///database.sqlite3"
class FrameType(Enum):
    INDEX = auto()
    TODAY = auto()
    PREVIEW = auto()


class EventType(Enum):
    FONT_CHANGED = auto()
    FS_CHANGED = auto()

    INDEX_BTN_CLICKED = auto()      # 全部
    TODAY_BTN_CLICKED = auto()      # 今天
    PREVIEW_BTN_CLICKED = auto()    # 近期
    CALANDER_BTN_CLICKED = auto()
    SETTINGS_BTN_CLICKED = auto()
    TAG_ADD_BTN_CLICKED = auto()

    MY_ITEMS_BTN_CLICKED = auto()

    ACTIVITY_ADD = auto()
    ACTIVITY_ADDED = auto()
    ACTIVITY_REMOVE = auto()
    ACTIVITY_REMOVED = auto()
    ACTIVITY_SELECTED = auto()
    ACTIVITIES_LOAD = auto()
    ACTIVITIES_LOADED = auto()

    TAG_ADD = auto()
    TAG_ADDED = auto()
    TAG_REMOVE = auto()
    TAG_REMOVED = auto()
    TAG_LOAD = auto()
    TAG_LOADED = auto()