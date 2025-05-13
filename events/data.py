from datetime import datetime
from enums.enums import FrameType
from models.local import Activity


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


class FontSizeChangedData(EventData):
    def __init__(self, font_size: int):
        super().__init__()
        self.font_size = font_size


class ActivityAddData(EventData):
    def __init__(self, starts_at: datetime, ends_at: datetime, description: str):
        super().__init__()
        self.starts_at = starts_at
        self.ends_at = ends_at
        self.description = description


class ActivityAddedData(ActivityAddData):
    def __init__(self, id_: int, starts_at, ends_at, description):
        super().__init__(starts_at, ends_at, description)
        self.id_ = id_


class ActivityRemoveData(EventData):
    def __init__(self, activity_id: int):
        super().__init__()
        self.activity_id = activity_id


class ActivityRemovedData(ActivityRemoveData):
    def __init__(self, activity_id: int):
        super().__init__(activity_id)


class ActivityGetData(EventData):
    def __init__(self):
        super().__init__()


class TagAddData(EventData):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class TagAddedData(TagAddData):
    def __init__(self, id_: int, name):
        super().__init__(name)
        self.id_ = id_


class TagRemoveData(EventData):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class TagRemovedData(TagRemoveData):
    def __init__(self, name):
        super().__init__(name)

class ActivitySelectedData(EventData):
    def __init__(self, id_: int | None):
        super().__init__()
        self.id_ = id_


class ActivitiesLoadData(EventData):
    def __init__(self, dt: datetime, tags: list[str] | None = None):
        super().__init__()
        self.dt = dt
        self.tags = tags

class ActivitiesLoadedData(EventData):
    def __init__(self, activities: list[Activity]):
        super().__init__()
        self.activities = activities


class TagSelectedData(EventData):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
