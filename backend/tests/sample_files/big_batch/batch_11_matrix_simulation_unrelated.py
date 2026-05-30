"""Completely different sample: matrix and cellular simulation utilities."""

import random


def create_grid(width, height, fill_value=0):
    grid = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(fill_value)
        grid.append(row)
    return grid


def seed_random_cells(grid, probability):
    for row_index, row in enumerate(grid):
        for col_index in range(len(row)):
            if random.random() < probability:
                grid[row_index][col_index] = 1
    return grid


def count_neighbors(grid, row, col):
    total = 0
    height = len(grid)
    width = len(grid[0])

    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if row_offset == 0 and col_offset == 0:
                continue

            next_row = row + row_offset
            next_col = col + col_offset

            if 0 <= next_row < height and 0 <= next_col < width:
                total += grid[next_row][next_col]

    return total


def next_generation(grid):
    updated = create_grid(len(grid[0]), len(grid), 0)

    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            neighbors = count_neighbors(grid, row_index, col_index)

            if cell == 1 and neighbors in (2, 3):
                updated[row_index][col_index] = 1
            elif cell == 0 and neighbors == 3:
                updated[row_index][col_index] = 1
            else:
                updated[row_index][col_index] = 0

    return updated


def simulate(grid, steps):
    history = []
    current = grid

    for step in range(steps):
        living_cells = sum(sum(row) for row in current)
        history.append({"step": step, "living_cells": living_cells})
        current = next_generation(current)

    return current, history


def grid_density(grid):
    total_cells = len(grid) * len(grid[0])
    living_cells = sum(sum(row) for row in grid)
    if total_cells == 0:
        return 0
    return living_cells / total_cells


def render_grid(grid):
    rendered_rows = []
    for row in grid:
        characters = []
        for cell in row:
            characters.append("#" if cell else ".")
        rendered_rows.append("".join(characters))
    return "\n".join(rendered_rows)


def find_stable_step(history):
    previous = None
    for item in history:
        if previous is not None and item["living_cells"] == previous:
            return item["step"]
        previous = item["living_cells"]
    return None


def run_demo():
    grid = create_grid(20, 12)
    seed_random_cells(grid, 0.28)
    final_grid, history = simulate(grid, 25)

    return {
        "density": round(grid_density(final_grid), 3),
        "stable_step": find_stable_step(history),
        "preview": render_grid(final_grid),
    }


if __name__ == "__main__":
    result = run_demo()
    print("Final density:", result["density"])
    print("Stable step:", result["stable_step"])
    print(result["preview"])
