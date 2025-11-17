import tkinter as tk
from tkinter import ttk

FONT_FAMILY = "Segoe UI"
FONT_SIZE = 20
FONT_SIZE_LARGE = 28

COLORS = {
    "primary": "#0d6efd",
    "secondary": "#6c757d",
    "text": "#eeeeee"
}

grid = None

def create_grid(window, rows, cols):
    entries = []

    for r in range(rows):
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

def select_equation_number(window, number):
    try:
        number = int(number)

        if number <= 1:
            raise ValueError
        
        destroy_all(window)
        render(window, number)
    
    except ValueError:
        # TODO
        print("ERROR!")


def render(window, equation_number=3):
    window.title("Equation Solver")
    window.minsize(1024, 768)

    # title
    main_label = ttk.Label(window, text="Equation Solver", font=(FONT_FAMILY, FONT_SIZE_LARGE))
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
                row.append(grid[r][c].get())
            values.append(row)
        
        # TODO
        print(values)

    solve_btn = tk.Button(
        window,
        command=get_values,
        bg=COLORS['primary'],
        fg=COLORS['text'],
        font=(FONT_FAMILY, FONT_SIZE),
        relief='flat',
        text='Solve',
        pady=2,
        padx=4
    )
    solve_btn.pack(pady=10)

    window.mainloop()


def destroy_all(window):
    for widget in window.winfo_children():
        widget.destroy()