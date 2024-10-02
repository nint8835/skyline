import io
from typing import Sequence

import cadquery


def skyline_model(days: Sequence[int | None]) -> str:
    grid = cadquery.Assembly()

    for index, count in enumerate(days):
        col_offset = 10 * (index // 7)
        row_offset = 10 * (index % 7)

        if count is None:
            continue

        grid.add(
            cadquery.Workplane("XY").box(10, 10, count + 2, centered=False),
            loc=cadquery.Location(cadquery.Vector(row_offset, col_offset, 0)),
        )

    skyline_workplane = (
        cadquery.Workplane("XY").center(0, 0).workplane().add(grid.toCompound())
    )

    out = io.StringIO()

    # TODO: exportShape is deprecated - find an alternative way of exporting a file without writing to disk
    cadquery.exporters.exportShape(skyline_workplane, "STL", out)  # type: ignore

    return out.getvalue()


__all__ = ["skyline_model"]
