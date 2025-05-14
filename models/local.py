from datetime import datetime

import json


class Activity:
    def __repr__(self):
        return json.dumps({
            'id': self.id_, 
            'starts_at': self.starts_at.strftime("%Y-%m-%d %H:%M"), 
            'ends_at': self.ends_at.strftime("%Y-%m-%d %H:%M"), 
            'description': self.description, 
            'done': self.done
        }, indent=4)
    

    def __init__(self, id_: int, starts_at: datetime, ends_at: datetime, description: str, tags: list["Tag"] | None = None, done: bool = False):
        self.id_ = id_
        self.starts_at = starts_at
        self.ends_at = ends_at
        self.description = description
        self.done = done

        self.tags = tags


class Tag:
    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)

    def __init__(self, id_: int, name: str, activities: list["Activity"] | None = None):
        self.id_ = id_
        self.name = name

        self.activities = activities