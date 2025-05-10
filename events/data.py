from datetime import datetime
from enums.enums import FrameType


'''
這邊放Event需要包起來的資料
'''


class EventData:
    def __init__(self):
        pass


class InputRowBtnClickedData(EventData):
    def __init__(self, frame_type: FrameType, value: str):
        super().__init__()
        self.frame_type = frame_type
        self.value = value


class IndexBtnClickedData(EventData):
    def __init__(self):
        super().__init__()


class MyItemsBtnClickedData(EventData):
    def __init__(self, tag: str):
        super().__init__()
        self.tag = tag


class Todo:
    def __init__(self, name: str, starts_at: datetime, ends_at: datetime):
        self.name = name
        self.starts = starts_at
        self.ends_at = ends_at