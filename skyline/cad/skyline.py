import math
import tempfile
from pathlib import Path
from typing import Self, Sequence

import cadquery

GRID_SQUARE_SIZE = 3
GRID_BASE_HEIGHT = 2

INTER_FONT_PATH = str(Path(__file__).parent / "fonts" / "Inter-Regular.ttf")


class PendingPolyline:
    def __init__(self):
        self.points: list[tuple[int, int]] = []

    def push(self, x: int, y: int) -> Self:
        # Do not push a point into the polyline if it is as the same location as the previous point
        # Doing so will result in a "BRep_API: command not done" error
        if len(self.points) > 0 and self.points[-1] == (x, y):
            return self

        self.points.append((x, y))
        return self


def skyline_model(
    *,
    days: Sequence[int | None],
    label: str | None = "",
    include_month_label: bool = True,
) -> bytes:
    cols = math.ceil(len(days) / 7.0)
    first_day_row = days.index(next(day for day in days if day is not None))
    # First week is None-padded, but last week is not None-padded
    # Therefore, to get the row of the last day we use the length of the last week
    last_day_row = len(days[7 * (cols - 1) :]) - 1

    base_polyline = PendingPolyline()

    (
        base_polyline
        # First week, top left
        .push(first_day_row * GRID_SQUARE_SIZE, 0)
        # First week, top right
        .push(first_day_row * GRID_SQUARE_SIZE, GRID_SQUARE_SIZE)
        # Second week, top left
        .push(0, GRID_SQUARE_SIZE)
        # Last week, top right
        .push(0, (cols + 1) * GRID_SQUARE_SIZE)
        # Last week, bottom right
        .push((last_day_row + 1) * GRID_SQUARE_SIZE, (cols + 1) * GRID_SQUARE_SIZE)
        # Last week, bottom left
        .push((last_day_row + 1) * GRID_SQUARE_SIZE, cols * GRID_SQUARE_SIZE)
        # Second last week, bottom right
        .push(7 * GRID_SQUARE_SIZE, cols * GRID_SQUARE_SIZE)
        # First week, bottom left
        .push(7 * GRID_SQUARE_SIZE, 0)
        # # First week, top left
        .push(first_day_row * GRID_SQUARE_SIZE, 0)
    )

    skyline_workplane = (
        cadquery.Workplane("XY")
        .polyline(base_polyline.points)
        .close()
        .extrude(GRID_BASE_HEIGHT)
    )

    # grid = cadquery.Assembly()

    # for index, count in enumerate(days):
    #     col_offset = (-GRID_SQUARE_SIZE * 52 / 2) + GRID_SQUARE_SIZE * (index // 7)
    #     row_offset = (-GRID_SQUARE_SIZE * 7 / 2) + GRID_SQUARE_SIZE * (index % 7)

    #     if count is None:
    #         continue

    #     grid.add(
    #         cadquery.Workplane("XY").box(
    #             GRID_SQUARE_SIZE,
    #             GRID_SQUARE_SIZE,
    #             count + GRID_BASE_HEIGHT,
    #             centered=False,
    #         ),
    #         loc=cadquery.Location(cadquery.Vector(row_offset, col_offset, 0)),
    #     )

    # skyline_workplane = (
    #     cadquery.Workplane("XY").center(0, 0).workplane().add(grid.toCompound())
    # )

    # if label:
    #     skyline_workplane = cast(
    #         cadquery.Workplane,
    #         skyline_workplane.faces("<Z")
    #         .workplane()
    #         .transformed(rotate=cadquery.Vector(0, 0, -90))
    #         .text(  # type: ignore - Decorator on .text currently breaks typing. PR opened to resolve this (https://github.com/CadQuery/cadquery/pull/1733)
    #             label,
    #             7.5,
    #             -1.0,
    #             fontPath=INTER_FONT_PATH,
    #         ),
    #     )

    # if include_month_label:
    #     skyline_workplane = cast(
    #         cadquery.Workplane,
    #         skyline_workplane.faces("<Z")
    #         .workplane()
    #         # TODO: Use a better way to position the label rather than a hardcoded offset
    #         .transformed(offset=cadquery.Vector(0, GRID_SQUARE_SIZE * 25, 0))
    #         .text(  # type: ignore - Decorator on .text currently breaks typing. PR opened to resolve this (https://github.com/CadQuery/cadquery/pull/1733)
    #             "Jan",
    #             7.5,
    #             -1.0,
    #             fontPath=INTER_FONT_PATH,
    #             valign="top",
    #         )
    #         # TODO: Use a better way to position the label rather than a hardcoded offset
    #         .transformed(
    #             offset=cadquery.Vector(0, GRID_SQUARE_SIZE * -51, 0),
    #             rotate=cadquery.Vector(0, 0, 180),
    #         )
    #         .text(  # type: ignore - Decorator on .text currently breaks typing. PR opened to resolve this (https://github.com/CadQuery/cadquery/pull/1733)
    #             "Dec",
    #             7.5,
    #             -1.0,
    #             fontPath=INTER_FONT_PATH,
    #             valign="top",
    #         ),
    #     )

    with tempfile.TemporaryDirectory(prefix="skyline_") as tmpdir:
        skyline_workplane.export(f"{tmpdir}/skyline.stl")

        with open(f"{tmpdir}/skyline.stl", "rb") as f:
            return f.read()


__all__ = ["skyline_model"]
