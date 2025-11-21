import tkinter as tk
from matrix import SYMBOLS, InfiniteSolutionsError, InconsistentSystemError
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

    if cols > 26:  # Use x1, x2, ..., xn if more than symbols
        for c in range(cols - 1):
            label = tk.Label(
                window,
                width=12,
                justify="center",
                fg=COLORS['primary'],
                font=(FONT_FAMILY, FONT_SIZE),
                text=f"X{c}"
            )
            label.grid(row=0, column=c, padx=3, pady=2)
    
    else:  # else, use x, y, z, w, a, b, c, ...
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

    if len(solutions) > 26:  # Use x1, x2, ..., xn if more than symbols
        for i in range(len(solutions)):
            label = tk.Label(
                solution_window,
                width=12,
                justify="center",
                font=(FONT_FAMILY, FONT_SIZE_LARGE),
                text=f"X{i} = {round(solutions[i], 4)}"
            )
            label.pack(anchor='center')
    
    else:  # else, use x, y, z, w, a, b, c, ...
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

    # -------------------------------------------------------
    # SCROLLABLE GRID AREA (Canvas + Scrollbars) - with centering
    # -------------------------------------------------------
    outer_frame = tk.Frame(window)
    outer_frame.pack(expand=True, fill="both")

    # scrollbars
    v_scroll = tk.Scrollbar(outer_frame, orient="vertical")
    h_scroll = tk.Scrollbar(outer_frame, orient="horizontal")
    v_scroll.pack(side="right", fill="y")
    h_scroll.pack(side="bottom", fill="x")

    # canvas
    canvas = tk.Canvas(
        outer_frame,
        yscrollcommand=v_scroll.set,
        xscrollcommand=h_scroll.set,
        highlightthickness=0
    )
    canvas.pack(side="left", fill="both", expand=True)

    v_scroll.config(command=canvas.yview)
    h_scroll.config(command=canvas.xview)

    # frame inside canvas (this will contain the grid)
    center_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=center_frame, anchor="nw")

    # When the content (center_frame) changes size, update scrollregion.
    def on_frame_configure(event=None):
        # Ask canvas to recompute scrollregion from content size
        center_frame.update_idletasks()
        fw = center_frame.winfo_reqwidth()
        fh = center_frame.winfo_reqheight()

        # Ensure scrollregion covers either the content size or the canvas size
        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        max_w = max(fw, cw)
        max_h = max(fh, ch)
        canvas.configure(scrollregion=(0, 0, max_w, max_h))

    center_frame.bind("<Configure>", on_frame_configure)

    # When the canvas itself resizes, center the frame inside it (if the canvas is larger).
    def on_canvas_configure(event):
        # sizes
        canvas_width = event.width
        canvas_height = event.height

        # make sure we have up-to-date requested size of the content
        center_frame.update_idletasks()
        frame_width = center_frame.winfo_reqwidth()
        frame_height = center_frame.winfo_reqheight()

        # compute top-left coords to center content (or 0 if content larger than canvas)
        x = max((canvas_width - frame_width) // 2, 0)
        y = max((canvas_height - frame_height) // 2, 0)

        # move the canvas window containing the frame
        canvas.coords(canvas_window, x, y)

        # update scrollregion too (keeps scrollbars consistent)
        max_w = max(frame_width + x, canvas_width)
        max_h = max(frame_height + y, canvas_height)
        canvas.configure(scrollregion=(0, 0, max_w, max_h))

    canvas.bind("<Configure>", on_canvas_configure)
    # -------------------------------------------------------

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
                    render_error(window, message="All coefficients must be non empty number.")
                    return

            values.append(row)
        
        try:
            solutions = solve(values, equation_number)
            render_solutions(window, solutions)
        
        except InconsistentSystemError:
            render_error(window, "The system is inconsistent.")
        
        except InfiniteSolutionsError:
            render_error(window, "The system has infinite number of solutions.")

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