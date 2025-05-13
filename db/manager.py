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
                raise ValueError("Cannot find the activity")
            session.delete(activity)
            session.commit()

    def modify_activity(self, activity_id: int, name: str, starts_at: datetime, ends_at: datetime) -> local.Activity:
        with Session(self._engine) as session:
            activity = session.query(db.Activity).filter(db.Activity.id_ == activity_id).first()
            if not activity:
                raise ValueError("Cannot find the activity")
            activity.name = name
            activity.starts_at = starts_at
            activity.ends_at = ends_at
            session.commit()
            local_activity = local.Activity(
                id_=activity.id_, 
                starts_at=activity.starts_at, 
                ends_at=activity.ends_at, 
                description=activity.name
            )
            return local_activity

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
            return local_activities
        
    def get_activity(self, id_: int | None) -> local.Activity | None:
        if not id_:
            return None
        with Session(self._engine) as session:
            activity = session.query(db.Activity).filter(db.Activity.id_ == id_).first()
            if not activity:
                return None
            return local.Activity(
                activity.id_, 
                activity.starts_at, 
                activity.ends_at, 
                activity.name
            )
        
    def add_tag(self, name: str) -> local.Tag:
        with Session(self._engine) as session:
            tag = db.Tag(name=name)
            session.add(tag)
            session.commit()
            tag_local = local.Tag(id_=tag.id_, name=tag.name, activities=[
                local.Activity(
                    id_=activity.id_, 
                    starts_at=activity.starts_at, 
                    ends_at=activity.ends_at, 
                    description=activity.name
                ) for activity in tag.activities
            ])
            return tag_local
        
    def remove_tag(self, name: str):
        with Session(self._engine) as session:
            tag = session.query(db.Tag).filter(db.Tag.name == name).first()
            if not tag:
                raise ValueError()
            session.delete(tag)
            session.commit()

    def get_tags(self):
        with Session(self._engine) as session:
            tags = session.query(db.Tag).all()
            local_tags = []
            for tag in tags:
                local_tags.append(local.Tag(
                    tag.id_, 
                    tag.name
                ))
            return local_tags
        
    def get_tag(self, name: str):
        with Session(self._engine) as session:
            tag = session.query(db.Tag).filter(db.Tag.name == name).first()
            if not tag:
                return None
            return local.Tag(
                tag.id_, 
                tag.name, 
                [local.Activity(
                    activity.id_, 
                    activity.starts_at, 
                    activity.ends_at
                ) for activity in tag.activities]
            )