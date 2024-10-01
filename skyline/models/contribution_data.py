from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from skyline.db import Base


class ContributionData(Base):
    __tablename__ = "contribution_data"

    user: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    contributions: Mapped[dict[str, int]] = mapped_column(JSON)
