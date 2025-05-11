from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from sqlalchemy import ForeignKey, Integer, String, DateTime, Table, Column
from datetime import datetime


class Base(DeclarativeBase):
    id_: Mapped[int] = mapped_column("id_", primary_key=True, autoincrement=True, unique=True, index=False, nullable=False)


activity_tags_table = Table(
    "activity_tags", 
    Base.metadata, 
    Column("activity_id", ForeignKey("activities.id_", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False), 
    Column("tag_id", ForeignKey("tags.id_", ondelete="CASCADE", onupdate="CASCADE"), unique=False, index=False, nullable=False)
)


class Activity(Base):
    __tablename__ = "activities"

    name: Mapped[str] = mapped_column(String, unique=False, index=False, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime, unique=False, index=False, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, unique=False, index=False, nullable=False)

    tags: Mapped[list["Tag"]] = relationship("Tag", activity_tags_table, uselist=True, back_populates="activities")


class Tag(Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column("name", unique=True, index=False, nullable=False)

    activities: Mapped[list["Activity"]] = relationship("Activity", activity_tags_table, uselist=True, back_populates="tags")

