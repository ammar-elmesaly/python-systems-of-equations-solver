import tkinter as tk
from matrix import SYMBOLS
from solver import solve

FONT_FAMILY = "Segoe UI"
FONT_SIZE = 20
FONT_SIZE_LARGE = 28

COLORS = {
    "primary": "#0d6efd",
    "secondary": "#6c757d",
    "error": "#dc3545",
    "text": "#eeeeee"
}

grid = None

def create_grid(window, rows, cols):
    entries = []

    for c in range(cols - 1):
        label = tk.Label(
            window,
            width=12,
            justify="center",
            fg=COLORS['primary'],
            font=(FONT_FAMILY, FONT_SIZE),
            text=SYMBOLS[c]
        )
        label.grid(row=0, column=c, padx=3, pady=2)

    for r in range(1, rows + 1):
        row_entries = []

        for c in range(cols):
            entry = tk.Entry(
                window,
                width=12,
                justify="center",
                bg=COLORS['secondary'],
                fg=COLORS['text'],
                font=(FONT_FAMILY, FONT_SIZE),
                relief='flat'
            )
            entry.grid(row=r, column=c, padx=3, pady=5)
            row_entries.append(entry)

        entries.append(row_entries)

    return entries


def render_error(window, message):
    error_window = tk.Toplevel(window)
    error_window.title("Error")
    error_window.minsize(600,300)
    error_window.resizable(False, False)  # Disable resizing window
    # Make the window modal (user must close it before interacting with main window)
    error_window.grab_set()
    error_window.transient(window)  # Keep the error window on top of the main window

    center_frame = tk.Frame(error_window)
    center_frame.pack(expand=True)

    error_label = tk.Label(center_frame, font=(FONT_FAMILY, FONT_SIZE))
    error_label.pack(anchor='center', padx=10, pady=2)

    error_task_btn = tk.Button(error_window,
            command=error_window.destroy,
            bg=COLORS["error"],
            fg=COLORS["text"],
            font=(FONT_FAMILY, FONT_SIZE),
            relief='flat',
            text='OK'
            )
    error_task_btn.pack(pady=30)

    error_label.configure(text=message)


def render_solutions(window, solutions: list[float]):
    solution_window = tk.Toplevel(window)
    solution_window.title("Solutions")
    solution_window.minsize(600,300)
    solution_window.resizable(False, True)
    # Make the window modal (user must close it before interacting with main window)
    solution_window.grab_set()
    solution_window.transient(window)  # Keep the error window on top of the main window

    for i in range(len(solutions)):
        label = tk.Label(
            solution_window,
            width=12,
            justify="center",
            font=(FONT_FAMILY, FONT_SIZE_LARGE),
            text=f"{SYMBOLS[i]} = {round(solutions[i], 4)}"
        )
        label.pack(anchor='center')


def select_equation_number(window, number):
    try:
        number = int(number)

        if number <= 1:
            raise ValueError
        
        destroy_all(window)
        render(window, number)
    
    except ValueError:
        render_error(window, message="Number of equations must be a valid integer > 1.")


def render(window, equation_number=3):
    window.title("Equation Solver")
    window.minsize(1024, 768)

    # title
    main_label = tk.Label(window, text="Equation Solver", font=(FONT_FAMILY, FONT_SIZE_LARGE))
    main_label.pack(pady=20)

    # select number of equations
    number_entry = tk.Entry(
        window,
        width=5,
        justify="center",
        font=(FONT_FAMILY, FONT_SIZE),
        relief='flat'
    )

    number_entry.insert(0, str(equation_number))
    number_entry.pack(pady=10)

    select_btn = tk.Button(
        window,
        command=lambda: select_equation_number(window, number_entry.get()),
        bg=COLORS['secondary'],
        fg=COLORS['text'],
        font=(FONT_FAMILY, FONT_SIZE),
        relief='flat',
        text='Select',
        pady=2,
        padx=3
    )
    select_btn.pack()


    center_frame = tk.Frame(window)
    center_frame.pack(expand=True)

    # equation grid
    grid = create_grid(center_frame, equation_number, equation_number + 1)

    def get_values():
        values = []
        for r in range(len(grid)):
            row = []
            for c in range(len(grid[r])):
                try:
                    row.append(float(grid[r][c].get()))
                except ValueError:
                    render_error(window, message="All coefficients must not be empty.")
                    return

            values.append(row)

        solutions = solve(values, equation_number)
        render_solutions(window, solutions)

    solve_btn = tk.Button(
        window,
        command=get_values,
        bg=COLORS['primary'],
        fg=COLORS['text'],
        font=(FONT_FAMILY, FONT_SIZE),
        relief='flat',
        text='Solve',
    )
    solve_btn.pack(padx=4, pady=80)

    window.mainloop()


def destroy_all(window):
    for widget in window.winfo_children():
        widget.destroy()