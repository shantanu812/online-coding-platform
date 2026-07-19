from datetime import  datetime, timezone
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base
from app.models.contest import Contest


class SubmissionStatus(str, Enum):
 
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SubmissionVerdict(str, Enum):
  
    ACCEPTED = "ACCEPTED"
    WRONG_ANSWER = "WRONG_ANSWER"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey(
            "problems.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[SubmissionStatus] = mapped_column(
        SqlEnum(
            SubmissionStatus,
            name="submission_status_enum",
        ),
        nullable=False,
        default=SubmissionStatus.PENDING,
    )

    verdict: Mapped[SubmissionVerdict | None] = mapped_column(
        SqlEnum(
            SubmissionVerdict,
            name="submission_verdict_enum",
        ),
        nullable=True,
    )

    execution_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    memory_used_kb: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    compiler_output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    submitted_at: Mapped[datetime] = mapped_column(
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

    user = relationship(
        "User",
        back_populates="submissions",
    )

    problem = relationship(
        "Problem",
        back_populates="submissions",
    )
    contest_id: Mapped[int | None] = mapped_column(
    ForeignKey("contests.id"),
    nullable=True,
    index=True,
    )

    contest: Mapped["Contest | None"] = relationship(
        "Contest",
        back_populates="submissions",
    )