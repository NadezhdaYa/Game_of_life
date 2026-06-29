"""
Генерация PNG-изображений поля. Цвет живой клетки зависит от возраста.
"""

from PIL import Image, ImageDraw
from typing import List, Tuple

Color = Tuple[int, int, int]

def interpolate_color(base_color: Color, age: int, max_age: int) -> Color:
    """
    Интерполяция от чёрного (0) к базовому цвету.
    Чем старше клетка, тем ближе её цвет к базовому.
    """
    if max_age == 0:
        return (0, 0, 0)
    factor = min(age, max_age) / max_age
    r = int(base_color[0] * factor)
    g = int(base_color[1] * factor)
    b = int(base_color[2] * factor)
    return (r, g, b)


def render_grid_to_png(
    grid: List[List[int]],
    path: str,
    cell_size: int = 10,
    base_color: Color = (255, 0, 0),
    dead_color: Color = (240, 240, 240),
    max_age_scale: int = 20,
) -> None:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    width = cols * cell_size
    height = rows * cell_size
    img = Image.new("RGB", (width, height), dead_color)
    draw = ImageDraw.Draw(img)

    for r in range(rows):
        for c in range(cols):
            age = grid[r][c]
            if age > 0:
                color = interpolate_color(base_color, age, max_age_scale)
                left = c * cell_size
                top = r * cell_size
                right = left + cell_size
                bottom = top + cell_size
                draw.rectangle([left, top, right, bottom], fill=color)

    img.save(path)