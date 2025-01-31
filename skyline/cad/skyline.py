import math
import tempfile
from pathlib import Path
from typing import Self, Sequence

import cadquery

GRID_SQUARE_SIZE = 3
GRID_BASE_HEIGHT = 2

INTER_FONT_PATH = str(Path(__file__).parent / "fonts" / "Inter-Regular.ttf")


class PendingPolyline:
    def __init__(self, offset_x: int | float = 0, offset_y: int | float = 0):
        self.points: list[tuple[int | float, int | float]] = []
        self.offset_x = offset_x
        self.offset_y = offset_y

    def push(self, x: int | float, y: int | float) -> Self:
        x += self.offset_x
        y += self.offset_y

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
    cols = math.floor(len(days) / 7.0)
    first_day_row = days.index(next(day for day in days if day is not None))
    # First week is None-padded, but last week is not None-padded
    # Therefore, to get the row of the last day we use the length of the last week
    last_day_row = len(days[7 * cols :]) - 1
    center_row_offset = -GRID_SQUARE_SIZE * 7 / 2
    center_col_offset = -GRID_SQUARE_SIZE * cols / 2

    base_polyline = PendingPolyline(center_row_offset, center_col_offset)

    #     C─────────────────────────────┬───D
    #     │                             │   │
    # A───B                             │   │
    # │   │                             │   │
    # │   │                             │   │
    # │   │                             │   │
    # │   │                             F───E
    # │   │                             │
    # H───┴─────────────────────────────G
    (
        base_polyline.push(first_day_row * GRID_SQUARE_SIZE, 0)  # A
        .push(first_day_row * GRID_SQUARE_SIZE, GRID_SQUARE_SIZE)  # B
        .push(0, GRID_SQUARE_SIZE)  # C
        .push(0, (cols + 1) * GRID_SQUARE_SIZE)  # D
        .push((last_day_row + 1) * GRID_SQUARE_SIZE, (cols + 1) * GRID_SQUARE_SIZE)  # E
        .push((last_day_row + 1) * GRID_SQUARE_SIZE, cols * GRID_SQUARE_SIZE)  # F
        .push(7 * GRID_SQUARE_SIZE, cols * GRID_SQUARE_SIZE)  # G
        .push(7 * GRID_SQUARE_SIZE, 0)  # H
        .push(first_day_row * GRID_SQUARE_SIZE, 0)  # A
    )

    skyline_workplane = (
        cadquery.Workplane("XY")
        .polyline(base_polyline.points)
        .close()
        .extrude(GRID_BASE_HEIGHT)
    )

    if label:
        skyline_workplane = (
            skyline_workplane.faces("<Z")
            .workplane()
            .transformed(rotate=cadquery.Vector(0, 0, -90))
            .text(
                label,
                7.5,
                -1.0,
                fontPath=INTER_FONT_PATH,
            )
        )

    if include_month_label:
        skyline_workplane = (
            skyline_workplane.faces("<Z")
            .workplane()
            # TODO: Use a better way to position the label rather than a hardcoded offset
            .transformed(
                offset=cadquery.Vector(0, -1 * center_col_offset - GRID_SQUARE_SIZE, 0)
            )
            .text(
                "Jan",
                7.5,
                -1.0,
                fontPath=INTER_FONT_PATH,
                valign="top",
            )
            # TODO: Use a better way to position the label rather than a hardcoded offset
            .transformed(
                offset=cadquery.Vector(0, 2 * center_col_offset + GRID_SQUARE_SIZE, 0),
                rotate=cadquery.Vector(0, 0, 180),
            )
            .text(
                "Dec",
                7.5,
                -1.0,
                fontPath=INTER_FONT_PATH,
                valign="top",
            )
        )

    grid = cadquery.Assembly()

    for index, count in enumerate(days):
        col_offset = center_col_offset + GRID_SQUARE_SIZE * (index // 7)
        row_offset = center_row_offset + GRID_SQUARE_SIZE * (index % 7)

        if not count:
            continue

        grid.add(
            cadquery.Workplane("XY").box(
                GRID_SQUARE_SIZE,
                GRID_SQUARE_SIZE,
                count,
                centered=False,
            ),
            loc=cadquery.Location(
                cadquery.Vector(row_offset, col_offset, GRID_BASE_HEIGHT)
            ),
        )

    skyline_workplane = skyline_workplane.add(grid.toCompound())

    with tempfile.TemporaryDirectory(prefix="skyline_") as tmpdir:
        skyline_workplane.export(f"{tmpdir}/skyline.stl")

        with open(f"{tmpdir}/skyline.stl", "rb") as f:
            return f.read()


__all__ = ["skyline_model"]
