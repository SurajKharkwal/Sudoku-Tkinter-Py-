
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("500x600")  # Set window size
        self.board: List[List[int]] = [[0 for _ in range(9)] for _ in range(9)]  # Sudoku board
        self.entries: List[List[Optional[tk.Entry]]] = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.add_buttons()

    def create_grid(self):
        """Create the game board."""
        validate_command = self.root.register(self.validate_entry)

        # Create a frame to hold the grid and center it
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=20)  # Center the grid with some padding

        # Create a 9x9 grid of Entry widgets
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(grid_frame, width=2, font=('Arial', 18), justify='center', validate="key",
                                 validatecommand=(validate_command, '%P'))
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

    def validate_entry(self, value):
        """Validation function for Entry widgets."""
        # Allow empty input (for deleting) or numbers 0-9
        return value == "" or (value.isdigit() and 0 <= int(value) <= 9)

    def get_board(self):
        """Get the current board values from the Entry widgets."""
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                if entry:  # Check if entry is not None
                    value = entry.get()
                    self.board[row][col] = int(value) if value else 0
                else:
                    self.board[row][col] = 0

    def set_board(self):
        """Set the Entry widgets based on the board state."""
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                entry = self.entries[row][col]
                if entry:  # Ensure entry is not None before interacting with it
                    entry.delete(0, tk.END)
                    if value != 0:
                        entry.insert(0, str(value))

    def is_valid(self, row, col, num):
        """Check if a number is valid in a specific cell."""
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        box_row, box_col = row // 3 * 3, col // 3 * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve(self):
        """Solve the Sudoku using backtracking."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def solve_board(self):
        """Get the board, solve it, and display the solution."""
        self.get_board()
        if self.solve():
            self.set_board()
            messagebox.showinfo("Success", "Sudoku Solved!")
        else:
            messagebox.showerror("Error", "No solution exists.")

    def reset_board(self):
        """Clear all entries on the board."""
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                if entry :
                    entry.delete(0, tk.END)

    def add_buttons(self):
        """Add Solve, Reset, and Generate Puzzle buttons."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)  # Center the buttons with padding

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_board)
        solve_button.grid(row=0, column=0, padx=10)

        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_board)
        reset_button.grid(row=0, column=1, padx=10)

        generate_button = tk.Button(button_frame, text="Generate Puzzle", command=self.generate_puzzle)
        generate_button.grid(row=0, column=2, padx=10)

    def generate_puzzle(self):
        """Generate a random Sudoku puzzle by removing numbers."""
        self.reset_board()
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve()
        num_cells_to_remove = random.randint(40, 60)  # Removing 40 to 60 cells
        for _ in range(num_cells_to_remove):
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0
        self.set_board()

def main():
    root = tk.Tk()
    SudokuGame(root)
    root.mainloop()

main()
