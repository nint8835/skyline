from datetime import date

from pydantic import BaseModel, Field


class ContributionsQueryContributionDay(BaseModel):
    date: date
    contribution_count: int = Field(alias="contributionCount")


class ContributionsQueryContributionWeek(BaseModel):
    contribution_days: list[ContributionsQueryContributionDay] = Field(
        alias="contributionDays"
    )


class ContributionsQueryContributionCalendar(BaseModel):
    weeks: list[ContributionsQueryContributionWeek]


class ContributionsQueryContributionCollection(BaseModel):
    contribution_calendar: ContributionsQueryContributionCalendar = Field(
        alias="contributionCalendar"
    )


class ContributionsQueryUser(BaseModel):
    contributions_collection: ContributionsQueryContributionCollection = Field(
        alias="contributionsCollection"
    )


class ContributionsQueryData(BaseModel):
    user: ContributionsQueryUser


class ContributionsQueryResponse(BaseModel):
    data: ContributionsQueryData


__all__ = ["ContributionsQueryResponse"]
