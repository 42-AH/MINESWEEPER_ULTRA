import random
import tkinter as tk
from tkinter import messagebox
import math

# TODO: Triangle grid

def generate_hex_grid(size, bomb_count):
    grid = {}
    for q in range(-size, size + 1):
        for r in range(-size, size + 1):
            if -q - r >= -size and -q - r <= size:  # Ensure valid hexagonal shape
                grid[(q, r)] = {'bomb': False, 'count': 0, 'revealed': False, 'flagged': False}

    # Place bombs
    all_cells = list(grid.keys())
    bomb_cells = random.sample(all_cells, bomb_count)
    for cell in bomb_cells:
        grid[cell]['bomb'] = True

    # Calculate bomb counts
    for (q, r) in grid.keys():
        if not grid[(q, r)]['bomb']:
            neighbors = [
                (q + 1, r), (q - 1, r), (q, r + 1),
                (q, r - 1), (q + 1, r - 1), (q - 1, r + 1)
            ]
            grid[(q, r)]['count'] = sum(
                grid.get(neighbor, {}).get('bomb', False) for neighbor in neighbors
            )

    return grid


class HexMinesweeper:
    def __init__(self, root, grid, size, hex_size=30):
        self.root = root
        self.grid = grid
        self.size = size
        self.hex_size = hex_size
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()
        self.cell_ids = {}  # To track hexagon IDs
        self.draw_grid()

    def draw_grid(self):
        for (q, r), cell in self.grid.items():
            self.draw_cell(q, r)

    def draw_cell(self, q, r):
        cell = self.grid[(q, r)]
        x, y = self.axial_to_pixel(q, r)
        points = self.get_hexagon_points(x, y)

        # Determine cell color (I like burlywood...)
        if cell['revealed']:
            fill_color = 'burlywood1' if (q + r) % 2 == 1 else 'burlywood3'
        elif cell['flagged']:
            fill_color = 'green' if (q + r) % 2 == 0 else 'darkgreen'
        else:
            # Alternate colors
            fill_color = 'green' if (q + r) % 2 == 0 else 'darkgreen'

        # Draw hexagon
        hex_id = self.canvas.create_polygon(points, fill=fill_color, outline='black')
        self.cell_ids[(q, r)] = hex_id

        # Add text for bombs, counting, or flags
        if cell['revealed']:
            if cell['bomb']:
                self.canvas.create_text(x, y, text="💣", fill='red', font=('Arial', 14))
            elif cell['count'] > 0:
                self.canvas.create_text(x, y, text=str(cell['count']), fill='blue', font=('Arial', 14))
        elif cell['flagged']:
            self.canvas.create_text(x, y, text="🚩", fill='red', font=('Arial', 14), tag=f"flag-{q}-{r}")

        # Bind events to the hexagon polygon only
        self.canvas.tag_bind(hex_id, "<Button-1>", lambda event, pos=(q, r): self.reveal_cell(pos))
        self.canvas.tag_bind(hex_id, "<Button-3>", lambda event, pos=(q, r): self.toggle_flag(pos))

    def axial_to_pixel(self, q, r):   # Axial is the system for having a hexagon grid
        size = self.hex_size
        x = size * 3 / 2 * q
        y = size * math.sqrt(3) * (r + q / 2)
        return x + 400, y + 300  # Center the grid

    def get_hexagon_points(self, x, y):
        size = self.hex_size
        return [
            (x + size * math.cos(angle), y + size * math.sin(angle))
            for angle in [(math.pi / 3) * i for i in range(6)]
        ]

    def reveal_cell(self, pos):
        if pos not in self.grid or self.grid[pos]['revealed'] or self.grid[pos]['flagged']:
            return
        cell = self.grid[pos]

        # If this is the first click and the cell is a bomb, switch the bomb somewhere else
        if cell['bomb'] and not any(c['revealed'] for c in self.grid.values()):
            # Find a non-bomb cell
            for target_pos, target_cell in self.grid.items():
                if not target_cell['bomb']:
                    # Swap
                    target_cell['bomb'] = True
                    cell['bomb'] = False
                    # Recalculate bomb counts
                    self.update_bomb_counts()
                    break

        cell['revealed'] = True
        if cell['bomb']:
            self.redraw_cell(pos)
            self.end_game(False)
        else:
            self.redraw_cell(pos)
            if cell['count'] == 0:
                self.reveal_neighbors(pos)

    def update_bomb_counts(self):
        # If we make the first click not a bomb, but it was, we have to recalculate
        for (q, r) in self.grid.keys():
            if not self.grid[(q, r)]['bomb']:
                neighbors = [
                    (q + 1, r), (q - 1, r), (q, r + 1),
                    (q, r - 1), (q + 1, r - 1), (q - 1, r + 1)
                ]
                self.grid[(q, r)]['count'] = sum(
                    self.grid.get(neighbor, {}).get('bomb', False) for neighbor in neighbors
                )

    def toggle_flag(self, pos):
        if pos not in self.grid or self.grid[pos]['revealed']:
            return
        cell = self.grid[pos]
        # Toggle the flag status
        cell['flagged'] = not cell['flagged']
        self.redraw_cell(pos)
        # Before this, clicking the actual ASCII flag wouldn't work
        if cell['flagged']:
            flag_tag = f"flag-{pos[0]}-{pos[1]}"
            self.canvas.tag_bind(flag_tag, "<Button-3>", lambda event, pos=pos: self.toggle_flag(pos))

    def redraw_cell(self, pos):
        # Update the cell's appearance
        q, r = pos
        self.canvas.delete(self.cell_ids[(q, r)])
        self.draw_cell(q, r)

        # Check if the game is won
        if all(cell['revealed'] or cell['bomb'] for cell in self.grid.values()):
            self.end_game(True)

    def reveal_neighbors(self, pos):
        q, r = pos
        neighbors = [
            (q + 1, r), (q - 1, r), (q, r + 1),
            (q, r - 1), (q + 1, r - 1), (q - 1, r + 1)
        ]
        for neighbor in neighbors:
            if neighbor in self.grid and not self.grid[neighbor]['revealed']:
                self.reveal_cell(neighbor)

    def end_game(self, won):
        message = "You Win!" if won else "You Lose!"
        messagebox.showinfo("Game Over", message)
        self.root.destroy()

