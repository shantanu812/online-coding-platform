from datetime import datetime

from sqlalchemy import ( 
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import ( 
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(
        primary_key=True,
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

    input: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_sample: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    problem = relationship(
        "Problem",
        back_populates="test_cases",
    )