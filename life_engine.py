"""
Логика игры «Жизнь»: правила Конвея, хранение возраста клеток.
"""
from typing import List, Tuple

Cell = Tuple[int, int]  # (row, col)

def count_neighbors(grid: List[List[int]], r: int, c: int) -> int:
    """Подсчитывает число живых соседей для клетки (r, c)."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] > 0:  # клетка жива, если age > 0
                    count += 1
    return count


def next_generation(grid: List[List[int]]) -> List[List[int]]:
    """Вычисляет следующее поколение по правилам Конвея.
    Возвращает новую сетку с возрастами клеток.
    Живые клетки получают age = 1, если родились; иначе age += 1.
    Мёртвые клетки — 0.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    new_grid = [[0] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(grid, r, c)
            is_alive = grid[r][c] > 0

            if is_alive:
                # выживание: 2 или 3 соседа
                if neighbors in (2, 3):
                    new_grid[r][c] = grid[r][c] + 1  # увеличиваем возраст
                else:
                    new_grid[r][c] = 0  # умирает
            else:
                # рождение: ровно 3 соседа
                if neighbors == 3:
                    new_grid[r][c] = 1  # новая клетка, возраст 1
                else:
                    new_grid[r][c] = 0

    return new_grid