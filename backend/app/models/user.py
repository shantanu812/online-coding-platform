from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.contest import Contest, contest_participants

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
    )

    submissions = relationship(
        "Submission",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    contests: Mapped[list["Contest"]] = relationship(
    "Contest",
    secondary=contest_participants,
    back_populates="participants",
    )

    created_contests: Mapped[list["Contest"]] = relationship(
        "Contest",
        foreign_keys="Contest.created_by",
        back_populates="creator",
    )