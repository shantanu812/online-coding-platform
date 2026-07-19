from datetime import datetime,timezone
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class ContestVisibility(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


contest_problems = Table(
    "contest_problems",
    Base.metadata,
    Column(
        "contest_id",
        ForeignKey("contests.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "problem_id",
        ForeignKey("problems.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


contest_participants = Table(
    "contest_participants",
    Base.metadata,
    Column(
        "contest_id",
        ForeignKey("contests.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "registered_at",
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False,
    ),
    UniqueConstraint(
        "contest_id",
        "user_id",
        name="uq_contest_participant",
    ),
)


class Contest(Base):
    __tablename__ = "contests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
    )

    visibility: Mapped[ContestVisibility] = mapped_column(
        SqlEnum(
            ContestVisibility,
            name="contest_visibility_enum",
        ),
        default=ContestVisibility.PUBLIC,
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
    )

    problems = relationship(
        "Problem",
        secondary=contest_problems,
        back_populates="contests",
    )

    participants = relationship(
        "User",
        secondary=contest_participants,
        back_populates="contests",
    )

    submissions = relationship(
        "Submission",
        back_populates="contest",
    )

    @property
    def status(self) -> str:
        now = datetime.now(timezone.utc)

        if now < self.start_time:
            return "UPCOMING"

        if now > self.end_time:
            return "FINISHED"

        return "RUNNING"