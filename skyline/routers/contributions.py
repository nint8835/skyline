from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from skyline.dependencies.auth import require_token, require_user
from skyline.dependencies.database import get_db
from skyline.tasks.importing import import_contributions

contributions_router = APIRouter(tags=["Contributions"])


@contributions_router.post(
    "/import/<year>",
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


__all__ = ["contributions_router"]
