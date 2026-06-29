"""
Точка входа: обработка аргументов, запуск симуляции, сохранение файлов и PNG.
"""

import argparse
import os
from life_engine import next_generation
from file_io import read_initial_grid, write_generations
from image_renderer import render_grid_to_png


def parse_color(color_args):
    if len(color_args) != 3:
        raise ValueError("--color требует 3 значения: R G B")
    r, g, b = map(int, color_args)
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("Компоненты цвета должны быть в диапазоне [0, 255].")
    return (r, g, b)


def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life CLI")
    parser.add_argument("--input", required=True, help="Путь к файлу начальной конфигурации.")
    parser.add_argument("--steps", type=int, required=True, help="Количество шагов симуляции.")
    parser.add_argument("--output", required=True, help="Путь к выходному текстовому файлу с историей поколений.")
    parser.add_argument("--png-prefix", required=True, help="Префикс имён PNG-файлов (например, frame).")
    parser.add_argument("--color", nargs=3, default=[255, 0, 0], help="Базовый цвет живых клеток (R G B).")
    parser.add_argument("--cell-size", type=int, default=10, help="Размер одной клетки в пикселях.")

    args = parser.parse_args()

    base_color = parse_color(args.color)

    # Чтение начальной конфигурации
    grid = read_initial_grid(args.input)
    generations = [grid]

    print(f"Начальное состояние прочитано: {len(grid)}x{len(grid[0])}")

    # Симуляция
    for step in range(1, args.steps + 1):
        grid = next_generation(grid)
        generations.append(grid)
        print(f"Шаг {step}/{args.steps} выполнен.")

    # Запись истории поколений
    write_generations(args.output, generations)
    print(f"История поколений сохранена в {args.output}")

    # Вычисляем глобальный максимум возраста по всем кадрам
    global_max_age = 0
    for gen in generations:
        for row in gen:
            for age in row:
                if age > global_max_age:
                    global_max_age = age

    # Защита от деления на ноль, если все клетки мертвы
    max_age_scale = global_max_age if global_max_age > 0 else 1
    print(f"Глобальный максимальный возраст: {max_age_scale}")

    # Генерация PNG для каждого поколения
    os.makedirs(os.path.dirname(args.png_prefix) or ".", exist_ok=True)
    for idx, gen in enumerate(generations):
        png_path = f"{args.png_prefix}_{idx:03d}.png"
        render_grid_to_png(
            gen, png_path,
            cell_size=args.cell_size,
            base_color=base_color,
            max_age_scale=max_age_scale
        )
        print(f"Сохранён кадр: {png_path}")


if __name__ == "__main__":
    main()