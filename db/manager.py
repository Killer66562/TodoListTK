from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session
from models import db, local
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_url: str):
        self._engine = create_engine(db_url)

    def add_activity(self, name: str, starts_at: datetime, ends_at: datetime) -> local.Activity:
        with Session(self._engine) as session:
            activity = db.Activity(name=name, starts_at=starts_at, ends_at=ends_at)
            session.add(activity)
            session.commit()
            local_activity = local.Activity(
                id_=activity.id_, 
                starts_at=activity.starts_at, 
                ends_at=activity.ends_at, 
                description=activity.name
            )
            return local_activity

    def remove_activity(self, activity_id: int):
        with Session(self._engine) as session:
            activity = session.query(db.Activity).filter(db.Activity.id_ == activity_id).first()
            if not activity:
                print("No activity")
            session.delete(activity)
            session.commit()

    def get_activities(self, starts_at: datetime | None, ends_at: datetime | None, tags: list[str] | None = None) -> list[local.Activity]:
        with Session(self._engine) as session:
            query = session.query(db.Activity)
            if starts_at and ends_at:
                query = query.filter(or_(
                    and_(db.Activity.starts_at >= starts_at, db.Activity.starts_at < starts_at + timedelta(days=1)), 
                    and_(db.Activity.ends_at >= ends_at, db.Activity.ends_at < ends_at + timedelta(days=1))
                ))
            elif starts_at:
                query = query.filter(db.Activity.starts_at >= starts_at, db.Activity.starts_at < starts_at + timedelta(days=1))
            elif ends_at:
                query = query.filter(db.Activity.ends_at >= ends_at, db.Activity.ends_at < ends_at + timedelta(days=1))
            activities = query.all()
            local_activities = [
                local.Activity(
                    id_=activity.id_, 
                    starts_at=activity.starts_at, 
                    ends_at=activity.ends_at, 
                    description=activity.name
                ) for activity in activities
            ]
            print(local_activities)
            return local_activities
        
    def add_tag(self, name: str) -> local.Tag:
        with Session(self._engine) as session:
            tag = db.Tag(name=name)
            session.add(tag)
            session.commit()
            tag_local = local.Tag(name=tag.name, activities=[
                local.Activity(
                    id_=activity.id_, 
                    starts_at=activity.starts_at, 
                    ends_at=activity.ends_at, 
                    description=activity.name
                ) for activity in tag.activities
            ])
            return tag_local