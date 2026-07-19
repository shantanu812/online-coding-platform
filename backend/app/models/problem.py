from datetime import datetime, timezone
from app.models.contest import Contest, contest_problems
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import ( 
    Boolean,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)


from app.database.base import Base


class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    statement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    difficulty: Mapped[Difficulty] = mapped_column(
        SqlEnum(Difficulty, name="difficulty_enum"),
        nullable=False,
    )

    time_limit_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1000,
    )

    memory_limit_mb: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=256,
    )

    input_format: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    output_format: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    constraints: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sample_input: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sample_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    creator = relationship("User", backref="created_problems")

    test_cases = relationship(
        "TestCase",
        back_populates="problem",
        cascade="all, delete-orphan",
    )
    submissions = relationship(
        "Submission",
        back_populates="problem",
        cascade="all, delete-orphan",
    )
    contests: Mapped[list["Contest"]] = relationship(
    "Contest",
    secondary=contest_problems,
    back_populates="problems",
    )