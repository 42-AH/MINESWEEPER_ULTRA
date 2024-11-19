import tkinter as tk
# from tkinter import ttk

from main import generate_hex_grid
from main import HexMinesweeper

class GameWindow(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Layout Test")
		self.protocol("WM_DELETE_WINDOW", self.quit_program)

		# Side Panel
		self.side_panel = tk.Frame(self)
		self.side_panel.grid(row=0, column=0)

		# Main Panel
		self.main_panel = tk.Frame(self)
		self.main_panel.grid(row=0, column=2)


		## ==============================
		## MARK: SIDE PANEL
		self.side_panel_title = tk.Label(self.side_panel, text="Lorem Ipsum, etc., ect.")
		self.side_panel_title.pack()

		## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

		## ==============================
		## MARK: Main PANEL
		self.main_panel_title = tk.Label(self.main_panel, text="< Hex Grid (placeholder) >")
		self.main_panel_title.pack()

		self.hex_grid = tk.Frame(self.main_panel)
		self.hex_grid.pack()

		game = HexMinesweeper(self.main_panel, generate_hex_grid(5, round(5 * 3.5)), 5)
		# TODO: Need to modify `HexMinesweeper` to not self-delete upon loss


		## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^




	def quit_program(self):
		self.destroy()


if __name__ == "__main__":
	app = GameWindow()
	app.mainloop()