from matrix import Mat

def solve(values: list[int], equation_number: int) -> list[float]:
    mat = Mat((equation_number, equation_number + 1))
    for row in values:
        mat.add_row(row)

    return mat.solve()