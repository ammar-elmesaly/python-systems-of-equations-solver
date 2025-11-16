import tkinter as tk
from tkinter import ttk, font
from tkinter import StringVar, IntVar

FONT_FAMILY = "Segoe UI"
FONT_SIZE = 20
FONT_SIZE_LARGE = 28

GRID_DIM = 3  # 3x3 Grid System (Dimensions)

COLORS = {
    "primary": "#0d6efd",
    "secondary": "#6c757d",
    "text": "#eeeeee"
}


def grid_window(window, grid_dim=GRID_DIM):  # This function configures grid weight

    cell_weight = 1

    for i in range(grid_dim):
        window.grid_rowconfigure(i, weight=cell_weight)  # ith Row
        window.grid_columnconfigure(i, weight=cell_weight)  # ith Column


def print_test():
    print("Hello World")


def render(window):
    # Configure Window

    window.title("Equation Solver")  # Start maximized
    window.minsize(800,600)  # Minumum width and height

    grid_window(window)

    main_label = ttk.Label(window, text="Equation Solver", font=(FONT_FAMILY, FONT_SIZE_LARGE))
    main_label.grid(row=0, column=1, sticky="N")

    solve_btn = tk.Button(window,
                    command=print_test,
                    bg=COLORS["primary"],
                    fg=COLORS["text"],
                    font=(FONT_FAMILY, FONT_SIZE),
                    relief='flat',
                    text='Create',
                    pady=2,
                    padx=4)
    
    solve_btn.grid(row=2, column=1, sticky="N")


    window.mainloop()