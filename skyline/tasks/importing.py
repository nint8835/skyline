from datetime import date
from typing import Any, Awaitable, Callable, cast

import httpx
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from skyline.dependencies.auth import oauth
from skyline.models.contribution_data import (
    ContributionData,
    ContributionImporter,
    Contributions,
)

from .importing_models import ContributionsQueryResponse

logger = structlog.get_logger()

CONTRIBUTIONS_QUERY = """
query ($user: String!, $start: DateTime!, $end: DateTime!) {
    user(login: $user) {
        contributionsCollection(from: $start, to: $end) {
            contributionCalendar {
                weeks {
                    contributionDays {
                        date
                        contributionCount
                    }
                }
            }
        }
    }
}
"""

type ContributionQuerier = Callable[[str, int], Awaitable[ContributionsQueryResponse]]


def oauth_contribution_querier(token: Any) -> ContributionQuerier:
    async def _contribution_querier(
        user: str,
        year: int,
    ) -> ContributionsQueryResponse:
        resp = cast(
            httpx.Response,
            await oauth.github.post(
                "/graphql",
                json={
                    "query": CONTRIBUTIONS_QUERY,
                    "variables": {
                        "user": user,
                        "start": f"{year}-01-01T00:00:00Z",
                        "end": f"{year}-12-31T23:59:59Z",
                    },
                },
                token=token,
            ),
        )
        resp.raise_for_status()

        return ContributionsQueryResponse.model_validate(resp.json())

    return _contribution_querier


async def import_year(
    user: str,
    year: int,
    importer: ContributionImporter,
    session: AsyncSession,
    querier: ContributionQuerier,
) -> None:
    logger.info("Importing contributions", user=user, year=year, importer=importer)

    data = await querier(user, year)

    simplified_contributions: dict[date, int] = {}
    total_contributions = 0

    for week in data.data.user.contributions_collection.contribution_calendar.weeks:
        for day in week.contribution_days:
            simplified_contributions[day.date] = day.contribution_count
            total_contributions += day.contribution_count

    async with session.begin():
        contributions = ContributionData(
            user=user,
            year=year,
            contributions=Contributions.model_validate(
                simplified_contributions
            ).model_dump_json(),
            importer=ContributionImporter.User,
        )
        session.add(contributions)

    logger.info(
        "Imported contributions",
        user=user,
        year=year,
        importer=importer,
        total_contributions=total_contributions,
    )


async def import_contributions(user: str, token: Any, session: AsyncSession) -> None:
    # TODO: Don't hardcode years
    # TODO: Handle years that are already imported
    # TODO: Do two import passes - one as the user, one as the bot
    for year in range(2016, 2024):
        await import_year(
            user,
            year,
            ContributionImporter.User,
            session,
            oauth_contribution_querier(token),
        )


__all__ = ["import_contributions"]
