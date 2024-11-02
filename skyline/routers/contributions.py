from datetime import date, datetime, timezone
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
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
from skyline.schemas.contributions import ModelContributionSelection
from skyline.tasks.importing import import_contributions

contributions_router = APIRouter(tags=["Contributions"])


async def fetch_year_contributions(
    user: str,
    year: int,
    db: AsyncSession,
    contribution_selection: ModelContributionSelection,
) -> list[int]:
    async with db.begin():
        user_contribution_data = (
            await db.execute(
                select(ContributionData).filter_by(
                    user=user, year=year, importer=ContributionImporter.User
                )
            )
        ).scalar_one_or_none()
        bot_contribution_data = (
            await db.execute(
                select(ContributionData).filter_by(
                    user=user, year=year, importer=ContributionImporter.Bot
                )
            )
        ).scalar_one_or_none()

    if not user_contribution_data or not bot_contribution_data:
        raise HTTPException(
            status_code=404, detail=f"Contributions not found for year {year}."
        )

    user_contributions = Contributions.model_validate_json(
        user_contribution_data.contributions
    )
    bot_contributions = Contributions.model_validate_json(
        bot_contribution_data.contributions
    )

    contributions = {}

    match contribution_selection:
        case ModelContributionSelection.All:
            contributions = bot_contributions.root
        case ModelContributionSelection.Personal:
            contributions = user_contributions.root
        case ModelContributionSelection.Work:
            for day in bot_contributions.root:
                contributions[day] = (
                    bot_contributions.root[day] - user_contributions.root[day]
                )

    return list(contributions.values())


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


@contributions_router.get("/model")
async def get_model(
    start_year: Annotated[int, Query(description="The start year for the model.")],
    end_year: Annotated[
        int | None, Query(description="The end year for the model.")
    ] = None,
    user: str = Depends(require_user),
    db: AsyncSession = Depends(get_db),
    contribution_selection: Annotated[
        ModelContributionSelection, Query(alias="contributions")
    ] = ModelContributionSelection.All,
    include_labels: bool = False,
):
    """Retrieve the contributions model for a given user and year."""
    if end_year is None:
        end_year = start_year

    if end_year < start_year:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponseSchema(
                detail="End year must be greater than or equal to start year."
            ).model_dump(),
        )

    days: list[int | None] = []

    for year in range(start_year, end_year + 1):
        days.extend(
            await fetch_year_contributions(user, year, db, contribution_selection)
        )

    # Pad the first week with None values to ensure the model is appropriately offset
    first_day = date(start_year, 1, 1)
    weekday_number = first_day.isoweekday()
    missing_days = weekday_number % 7
    days = [None] * missing_days + days

    model = skyline_model(
        days=days,
        label=f"{user}\n{year} - {contribution_selection.value.capitalize()} Contributions"
        if include_labels
        else None,
        include_month_label=include_labels,
    )

    return Response(
        model,
        headers={
            "Content-Type": "model/stl",
            "Content-Disposition": f"attachment; filename={user}-{start_year}-{end_year}.stl",
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


@contributions_router.get("/work-contributions-available/{year}")
async def work_contributions_available(
    year: int, user: str = Depends(require_user), db: AsyncSession = Depends(get_db)
) -> bool:
    """Get whether or not work contributions are available for the user for."""
    async with db.begin():
        user_contribution_data = (
            await db.execute(
                select(ContributionData).filter_by(
                    user=user, year=year, importer=ContributionImporter.User
                )
            )
        ).scalar_one_or_none()
        bot_contribution_data = (
            await db.execute(
                select(ContributionData).filter_by(
                    user=user, year=year, importer=ContributionImporter.Bot
                )
            )
        ).scalar_one_or_none()

    if not user_contribution_data or not bot_contribution_data:
        return False

    return (
        Contributions.model_validate_json(bot_contribution_data.contributions).root
        != Contributions.model_validate_json(user_contribution_data.contributions).root
    )


__all__ = ["contributions_router"]
