import tkinter as tk
from tkinter import messagebox
import random

def find_empty_location(grid):
    # Find empty location in the Sudoku grid
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None


def is_valid_location(grid, row, col, num):
    # Check if num is already in row
    for i in range(9):
        if grid[row][i] == num:
            return False

    # Check if num is already in column
    for i in range(9):
        if grid[i][col] == num:
            return False

    # Check if num is already in 3x3 box
    box_row = row - row % 3
    box_col = col - col % 3
    for i in range(box_row, box_row+3):
        for j in range(box_col, box_col+3):
            if grid[i][j] == num:
                return False

    return True

def solver():
    root = tk.Tk()
    root.configure(bg="#FDF7C3", padx=100, pady=100, borderwidth=10, relief="solid")
    root.geometry("500x600+500+150")
    root.title("Sudoku Solver")

    # Create a 2D array of entry widgets
    entry_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            entry = tk.Entry(root, width=2, font=('Arial', 16))
            entry.grid(row=i, column=j, padx=3, pady=3)
            row.append(entry)
        entry_grid.append(row)

    # Add solve button
    button_solve = tk.Button(
        root, text="Solve", borderwidth=3, background="peach puff3", command=lambda: solve_sudoku_gui(entry_grid))
    button_solve.grid(row=12, column=4)

    root.mainloop()

def is_valid_location_and_not_zero(grid, row, col, num):
    if num == 0:
        return True
    # Check if num is already in row
    count = 0
    for i in range(9):
        if grid[row][i] == num:
            count += 1
    if count > 1:
        return False, (i, 'row')

    count = 0
    # Check if num is already in column
    for i in range(9):
        if grid[i][col] == num:
            count += 1
    if count > 1:
        return False, (i, 'col')

    count = 0
    # Check if num is already in 3x3 box
    box_row = row - row % 3
    box_col = col - col % 3
    for i in range(box_row, box_row+3):
        for j in range(box_col, box_col+3):
            if grid[i][j] == num:
                count += 1
    if count > 1:
        return False, (i, j)

    return True, 'Passed'

valid = False
temp_count = 0
def solve_sudoku(grid):
    global valid, temp_count
    # Find empty location in the Sudoku grid
    empty_loc = find_empty_location(grid)
    temp_count += 1
    if temp_count > 500:
        return

    # If no empty location exists, Sudoku is solved
    if not empty_loc:
        return True

    # Get the row and column of the empty location
    row, col = empty_loc

    # Try each number from 1 to 9 in the empty location
    for num in range(1, 10):
        valid_return = is_valid_location(grid, row, col, num)
        if valid_return:
            # If the number is valid, fill it in the empty location
            grid[row][col] = num

            # Recursively solve the remaining Sudoku puzzle
            if solve_sudoku(grid):
                return True

            # If the remaining Sudoku puzzle cannot be solved with this number, backtrack
            grid[row][col] = 0
        else:
            if valid != True:
                duplicate_valid_return, place = is_valid_location_and_not_zero(grid, row, col, num)
                if not duplicate_valid_return:
                    valid = True
                    messagebox.showerror(title="Invalid Input", message="Your input is invalid ❌")

    # If no number from 1 to 9 works, backtrack
    return False

def solve_sudoku_gui(entry_grid):
    global temp_count, valid
    # Get the input grid from the entry widgets
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            if isinstance(entry_grid[i][j], tk.Entry):
                val = int(entry_grid[i][j].get()
                          ) if entry_grid[i][j].get() else 0
            else:
                val = int(entry_grid[i][j].cget('text')
                          ) if entry_grid[i][j].cget('text') else 0
            row.append(val)
        grid.append(row)

    # Solve the Sudoku puzzle using the solve_sudoku function
    valid = False
    temp_count = 0
    if solve_sudoku(grid):
        # If solution found, update the entry widgets
        for i in range(9):
            for j in range(9):
                if isinstance(entry_grid[i][j], tk.Entry):
                    entry_grid[i][j].delete(0, tk.END)
                    entry_grid[i][j].insert(0, str(grid[i][j]))
                else:
                    entry_grid[i][j].configure(text=str(grid[i][j]))
    else:
        # no solution, show an error
        messagebox.showerror("Error", "No solution exists")


def generate_sudoku_puzzle():
    # a partially-filled 9x9 grid
    grid = [[0 for j in range(9)] for i in range(9)]

    # Fill some initial values
    for i in range(20):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)

        if is_valid_location(grid, row, col, num):
            grid[row][col] = num

    num_to_remove = 35

    for i in range(num_to_remove):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0

    return grid

def is_valid_sudoku(grid):

    # Check row
    for i in range(9):
        row_set = set()
        for j in range(9):
            if grid[i][j] == 0:
                continue
            if grid[i][j] in row_set:
                return False
            row_set.add(grid[i][j])

    # Check col
    for j in range(9):
        col_set = set()
        for i in range(9):
            if grid[i][j] == 0:
                continue
            if grid[i][j] in col_set:
                return False
            col_set.add(grid[i][j])

    # check 3x3 box
    for k in range(9):
        subgrid_set = set()
        for i in range(k // 3 * 3, k // 3 * 3 + 3):
            for j in range(k % 3 * 3, k % 3 * 3 + 3):
                if grid[i][j] == 0:
                    continue
                if grid[i][j] in subgrid_set:
                    return False
                subgrid_set.add(grid[i][j])

    # If all checks pass, Sudoku valid
    return True

def check_sudoku_gui(entry_grid):
    # Getting input from the entry box
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            if isinstance(entry_grid[i][j], tk.Entry):
                val = int(entry_grid[i][j].get()) if entry_grid[i][j].get() else 0
            else:
                val = int(entry_grid[i][j].cget('text')) if entry_grid[i][j].cget('text') else 0
            row.append(val)
        grid.append(row)

    valid = is_valid_sudoku(grid)

    # Showing message box
    if valid:
        messagebox.showinfo(title="Validity Info", message="The input is valid ✔️")
    else:
        messagebox.showerror(title="Validity Info", message="The input is not valid ❌")

def game():

    root = tk.Tk()
    root.configure(bg="#FDF7C3", padx=90, pady=140, borderwidth=10, relief="solid")
    root.geometry("500x600+500+150")
    root.title("Sudoku Solver")

    # partially-filled Sudoku
    grid = generate_sudoku_puzzle()

    # Create a 2D array
    entry_grid = []
    for i in range(9):
        row = []
        for j in range(9):
            if grid[i][j] != 0:
                # If value pre-filled, create label
                label = tk.Label(root, text=str(
                    grid[i][j]), font=('Arial', 16))
                label.grid(row=i, column=j, padx=1, pady=1)
                row.append(label)
            else:
                # If value not pre-filled, create entry widget
                entry = tk.Entry(root, width=2, font=('Arial', 16))
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
        entry_grid.append(row)

    # Add solve button
    button_solve = tk.Button(
        root, text="Solve", borderwidth=1, background="peach puff3", command=lambda: solve_sudoku_gui(entry_grid))
    button_solve.grid(row=10, column=3)

    # Add check button
    button_solve = tk.Button(
        root, text="Check", borderwidth=1, background="peach puff3", command=lambda: check_sudoku_gui(entry_grid))
    button_solve.grid(row=10, column=5)

    root.mainloop()

# Create Tkinter window
root = tk.Tk()
root.configure(bg="#FDF7C3", padx=90, pady=140, borderwidth=10, relief="solid")
root.title("Sudoku Puzzle")
root.geometry("425x500+500+150")
root.resizable(width=False, height=False)
MyLabel = tk.Label(root, text="SUDOKU PUZZLE", background="peach puff3", borderwidth=4, relief="solid", font=30, width=20, height=2)
MyLabel.grid(row=0, column=5)

button_solve = tk.Button(root, text="Solver", borderwidth=8, background="peach puff3", command=solver, height=2,width=18)
button_solve.grid(row=9, column=5)

button_game = tk.Button(root, text="Play Game", borderwidth=8, background="peach puff3", command=game, height=2,width=18)
button_game.grid(row=10, column=5)

root.mainloop()