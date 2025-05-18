from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import Session
from models import db, local
from datetime import date, datetime, timedelta

class DatabaseManager:
    def __init__(self, db_url: str):
        self._engine = create_engine(db_url)

    def add_activity(self, name: str, starts_at: datetime, ends_at: datetime, tags: list[local.Tag] | None = None) -> local.Activity:
        with Session(self._engine) as session:
            activity = db.Activity(name=name, starts_at=starts_at, ends_at=ends_at)
            session.add(activity)
            if tags:
                for tag in tags:
                    db_tag = session.query(db.Tag).filter(db.Tag.id_ == tag.id_).first()
                    if db_tag:
                        activity.tags.append(db_tag)
            session.commit()
            local_activity = local.Activity(
                id_=activity.id_, 
                starts_at=activity.starts_at, 
                ends_at=activity.ends_at, 
                description=activity.name, 
                done=activity.done
            )
            return local_activity

    def remove_activity(self, activity_id: int):
        with Session(self._engine) as session:
            activity = session.query(db.Activity).filter(db.Activity.id_ == activity_id).first()
            if not activity:
                raise ValueError("Cannot find the activity")
            session.delete(activity)
            session.commit()

    def modify_activity(self, activity_id: int, name: str, starts_at: datetime, ends_at: datetime, done: bool, tags: list[local.Tag] | None = None) -> local.Activity:
        with Session(self._engine) as session:
            activity = session.query(db.Activity).filter(db.Activity.id_ == activity_id).first()
            if not activity:
                raise ValueError("Cannot find the activity")
            activity.name = name
            activity.starts_at = starts_at
            activity.ends_at = ends_at
            activity.done = done
            activity.tags.clear()
            if tags:
                for tag in tags:
                    db_tag = session.query(db.Tag).filter(db.Tag.id_ == tag.id_).first()
                    if db_tag:
                        activity.tags.append(db_tag)
            session.commit()
            local_activity = local.Activity(
                id_=activity_id, 
                starts_at=starts_at, 
                ends_at=ends_at, 
                description=name, 
                done=done
            )
            return local_activity

    def get_activities(self, d: date | None = None, tags: list[str] | None = None, done: bool | None = None, e_filt: bool | None = None) -> list[local.Activity]:
        with Session(self._engine) as session:
            query = session.query(db.Activity)

            if done is not None:
                query = query.filter(db.Activity.done == done)

            if d is not None:
                dt_1 = datetime(d.year, d.month, d.day, 0, 0, 0)
                dt_2 = datetime(d.year, d.month, d.day, 23, 59, 59)

                if e_filt is None:
                    query = query.filter(
                        or_(
                            and_(db.Activity.starts_at >= dt_1, db.Activity.starts_at <= dt_2), 
                            and_(db.Activity.ends_at >= dt_1, db.Activity.ends_at <= dt_2), 
                            and_(dt_1 > db.Activity.starts_at, dt_1 < db.Activity.ends_at)
                        )
                    )
                elif e_filt is True:
                    query = query.filter(
                        and_(db.Activity.ends_at >= dt_1, db.Activity.ends_at <= dt_2)
                    )
                elif e_filt is False:
                    query = query.filter(
                        and_(db.Activity.starts_at >= dt_1, db.Activity.starts_at <= dt_2)
                    )

            if tags:
                for tag in tags:
                    query = query.filter(db.Activity.tags.any(name=tag))

            activities = query.all()
            local_activities = [
                local.Activity(
                    id_=activity.id_, 
                    starts_at=activity.starts_at, 
                    ends_at=activity.ends_at, 
                    description=activity.name, 
                    done=activity.done
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
                activity.name, 
                done=activity.done, 
                tags=[local.Tag(
                    tag.id_, 
                    tag.name
                ) for tag in activity.tags]
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
                    description=activity.name, 
                    done=activity.done
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
                    activity.ends_at, 
                    done=activity.done
                ) for activity in tag.activities]
            )