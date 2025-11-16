from matrix import Mat

def main():
    mat = Mat((2, 3))
    mat.add_row([1, 1, 8])
    mat.add_row([1, -1, 2])

    mat.solve()

if __name__ == "__main__":
    main()