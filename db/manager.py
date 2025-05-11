from sqlalchemy.engine import  Engine
from sqlalchemy.orm import Session
from models.models import Activity
from datetime import datetime, timedelta


class ActivitiesManager:
    def __init__(self, engine: Engine):
        self._engine = engine

    def add_activity(self, name: str, starts_at: datetime, ends_at: datetime):
        with Session(self._engine) as session:
            activity = Activity(name=name, starts_at=starts_at, ends_at=ends_at)
            session.add(activity)
            session.commit()

    def remove_activity(self, activity_id: int):
        with Session(self._engine) as session:
            activity = session.query(Activity).filter(Activity.id_ == activity_id).first()
            if not activity:
                return
            session.delete(activity)
            session.commit()
