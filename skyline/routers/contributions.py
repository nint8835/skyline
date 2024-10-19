from datetime import datetime, timezone
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, Path, Response, status
from fastapi.responses import JSONResponse
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
from skyline.schemas import ErrorResponseSchema
from skyline.tasks.importing import import_contributions

contributions_router = APIRouter(tags=["Contributions"])


@contributions_router.post(
    "/import/{year}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Year",
            "model": ErrorResponseSchema,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated",
            "model": ErrorResponseSchema,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Contributions Already Imported",
            "model": ErrorResponseSchema,
        },
    },
)
async def start_import(
    year: Annotated[int, Path(description="The year to import contributions for.")],
    user: str = Depends(require_user),
    token: Any = Depends(require_token),
    db: AsyncSession = Depends(get_db),
):
    """Import contributions for the current user."""

    if year >= datetime.now(timezone.utc).year or year < 2005:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponseSchema(
                detail="Invalid year. Year must be greater than or equal to 2005, and less than the current year."
            ).model_dump(),
        )

    async with db.begin():
        is_imported = (
            await db.execute(
                select(ContributionData).filter_by(user=user, year=year).limit(1)
            )
        ).scalar_one_or_none()
        if is_imported:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=ErrorResponseSchema(
                    detail="Contributions already imported."
                ).model_dump(),
            )

    await import_contributions(user, year, token, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@contributions_router.get("/model/{year}", include_in_schema=False)
async def get_model(
    year: int,
    user: str = Depends(require_user),
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


@contributions_router.get("/years")
async def get_years(
    user: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
) -> Sequence[int]:
    """Get a list of years for which contributions have been imported."""
    async with db.begin():
        years = (
            (
                await db.execute(
                    select(ContributionData.year).filter_by(user=user).distinct()
                )
            )
            .scalars()
            .all()
        )

    return years


__all__ = ["contributions_router"]
