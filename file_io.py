"""
Чтение начальной конфигурации и запись истории поколений.
"""

from typing import List

def read_initial_grid(path: str) -> List[List[int]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    if not lines:
        raise ValueError("Пустой входной файл.")

    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("Первая строка должна содержать ROWS COLS.")
    rows, cols = map(int, header)

    grid = []
    for i, line in enumerate(lines[1:], start=1):
        if len(line) != cols:
            raise ValueError(f"Строка {i} имеет длину {len(line)}, ожидалось {cols}.")
        row = [1 if ch == "#" else 0 for ch in line]
        grid.append(row)

    if len(grid) != rows:
        raise ValueError(f"Ожидали {rows} строк с данными, получили {len(grid)}.")

    return grid


def write_generations(path: str, generations: List[List[List[int]]]) -> None:
    """Записывает все поколения в текстовый файл, разделяя их строкой ---."""
    with open(path, "w", encoding="utf-8") as f:
        for idx, grid in enumerate(generations):
            if idx > 0:
                f.write("---\n")
            rows = len(grid)
            cols = len(grid[0]) if rows > 0 else 0
            f.write(f"{rows} {cols}\n")
            for row in grid:
                line = "".join("#" if cell > 0 else "." for cell in row)
                f.write(line + "\n")