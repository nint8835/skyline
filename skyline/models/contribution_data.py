from datetime import date
from enum import Enum

from pydantic import RootModel
from sqlalchemy.orm import Mapped, mapped_column

from skyline.db import Base

Contributions = RootModel[dict[date, int]]


class ContributionImporter(Enum):
    User = "user"
    Bot = "bot"


class ContributionData(Base):
    __tablename__ = "contribution_data"

    user: Mapped[str] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(primary_key=True)
    contributions: Mapped[str]
    importer: Mapped[ContributionImporter]


__all__ = ["Contributions", "ContributionData", "ContributionImporter"]
