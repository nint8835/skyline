import tempfile
from pathlib import Path
from typing import Sequence, cast

import cadquery

GRID_SQUARE_SIZE = 3
GRID_BASE_HEIGHT = 2


def skyline_model(*, days: Sequence[int | None], label: str | None = "") -> bytes:
    grid = cadquery.Assembly()

    for index, count in enumerate(days):
        col_offset = (-GRID_SQUARE_SIZE * 52 / 2) + GRID_SQUARE_SIZE * (index // 7)
        row_offset = (-GRID_SQUARE_SIZE * 7 / 2) + GRID_SQUARE_SIZE * (index % 7)

        if count is None:
            continue

        grid.add(
            cadquery.Workplane("XY").box(
                GRID_SQUARE_SIZE,
                GRID_SQUARE_SIZE,
                count + GRID_BASE_HEIGHT,
                centered=False,
            ),
            loc=cadquery.Location(cadquery.Vector(row_offset, col_offset, 0)),
        )

    skyline_workplane = (
        cadquery.Workplane("XY").center(0, 0).workplane().add(grid.toCompound())
    )

    if label:
        skyline_workplane = cast(
            cadquery.Workplane,
            skyline_workplane.faces("<Z")
            .workplane()
            .transformed(rotate=cadquery.Vector(0, 0, -90))
            .text(  # type: ignore - Decorator on .text currently breaks typing. PR opened to resolve this (https://github.com/CadQuery/cadquery/pull/1733)
                label,
                7.5,
                -1.0,
                fontPath=str(Path(__file__).parent / "fonts" / "Inter-Regular.ttf"),
            ),
        )

    with tempfile.TemporaryDirectory(prefix="skyline_") as tmpdir:
        skyline_workplane.export(f"{tmpdir}/skyline.stl")

        with open(f"{tmpdir}/skyline.stl", "rb") as f:
            return f.read()


__all__ = ["skyline_model"]
