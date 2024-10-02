from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from skyline.cad.skyline import skyline_model
from skyline.dependencies.auth import require_token, require_user
from skyline.dependencies.database import get_db
from skyline.models.contribution_data import (
    ContributionData,
    ContributionImporter,
    Contributions,
)
from skyline.tasks.importing import import_contributions

contributions_router = APIRouter(tags=["Contributions"])


@contributions_router.post(
    "/import/{year}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def start_import(
    year: int,
    background_tasks: BackgroundTasks,
    user: str = Depends(require_user),
    token: Any = Depends(require_token),
    db: AsyncSession = Depends(get_db),
):
    """Import contributions for the current user."""
    background_tasks.add_task(import_contributions, user, year, token, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@contributions_router.get("/model/{user}/{year}")
async def get_model(
    user: str,
    year: int,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve the contributions model for a given user and year."""
    async with db.begin():
        contribution_data = (
            await db.execute(
                select(ContributionData).filter_by(
                    user=user, year=year, importer=ContributionImporter.User
                )
            )
        ).scalar_one_or_none()

    if not contribution_data:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    contributions = Contributions.model_validate_json(contribution_data.contributions)
    days = list(contributions.root.values())

    # Pad the first week with None values to ensure the model is appropriately offset
    first_day = list(contributions.root.keys())[0]
    weekday_number = first_day.isoweekday()
    missing_days = weekday_number % 7
    days = [None] * missing_days + days

    model = skyline_model(days)

    return Response(
        model,
        headers={
            "Content-Type": "model/stl",
            "Content-Disposition": f"attachment; filename={user}-{year}.stl",
        },
    )


__all__ = ["contributions_router"]
