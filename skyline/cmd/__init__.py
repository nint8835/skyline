import logging

import alembic.config
import structlog
import typer
import uvicorn

from skyline.config import config

structlog.stdlib.recreate_defaults(log_level=logging.WARNING)
structlog.stdlib.get_logger("skyline").setLevel(
    logging.getLevelNamesMapping()[config.log_level]
)

app = typer.Typer()


@app.command()
def start() -> None:
    """Run Skyline."""

    uvicorn.run(
        "skyline.app:app",
        host=config.bind_host,
        port=config.bind_port,
        proxy_headers=config.behind_reverse_proxy,
        forwarded_allow_ips="*" if config.behind_reverse_proxy else None,
    )


@app.command()
def upgrade() -> None:
    """Perform database migrations."""
    alembic.config.main(argv=["--raiseerr", "upgrade", "head"])


__all__ = ["app"]
