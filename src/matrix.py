SYMBOLS = "xyzwabcdefghijklmnopqrstuv"
print_matrix_dbg = True

class InfiniteSolutionsError(Exception):
    # The system has infinitely many solutions.
    pass


class InconsistentSystemError(Exception):
    # The system has no solution.
    pass


class Mat:
    def __init__(self, size):
        self.size = size
        self._data = []


    def add_row(self, row):
        if len(self._data) > self.size[0] - 1:
            raise IndexError("Matrix out of range")
        
        if len(row) != self.size[1]:
            raise ValueError("Matrix row length error")
        
        self._data.append(row)

    def swap_rows(self, r1, r2):
        temp = self.get_row(r1)
        self._data[r1] = self.get_row(r2)
        self._data[r2] = temp
        print(f"Swapped R{r1 + 1} and R{r2 + 1}")
        self.print_matrix_dbg()


    def print(self):
        for row in self._data:
            for col in row:
                print(f"{col} ", end="")
            print()
    

    def divide(self, row, num):
        for i in range(self.size[1]):
            self._data[row][i] = self.get_row(row)[i] / num
        
        print(f"Divided R{row + 1} by {num}")
        self.print_matrix_dbg()


    def multiply(self, row, num):
        for i in range(self.size[1]):
            self._data[row][i] = self.get_row(row)[i] * num
        
        print(f"Multiplied R{row + 1} by {num}")
        self.print_matrix_dbg()

    def sum(self, r1, r2):
        for i in range(self.size[1]):
            self._data[r1][i] += self.get_row(r2)[i]
        
        print(f"R{r1 + 1} -> R{r1 + 1} + R{r2 + 1}")
        self.print_matrix_dbg()
    

    def multiply_then_sum(self, r1, r2, num):
        for i in range(self.size[1]):
            self._data[r1][i] += num * self.get_row(r2)[i]
        
        print(f"R{r1 + 1} -> R{r1 + 1} + {num} x R{r2 + 1}")
        self.print_matrix_dbg()

    def get_row(self, row):
        return self._data[row]
        

    def copy_matrix(self):
        result = Mat(self.size)

        for row in self._data:
            result.add_row(row.copy())
        
        return result


    def find_nonzero_lead(self, start, col):  # This searches for nonzero lead in a specific column
        for r in range(start, self.size[0]):
            if self.get_row(r)[col] != 0:
                return r
        
        return -1
    

    def is_inconsistent_row(self, row):
        for i in range(self.size[1] - 1):
            if self.get_row(row)[i] != 0:
                return False
        
        if self.get_row(row)[-1] == 0:
            return False
        
        return True



    def is_inconsistent(self):
        for r in range(self.size[0]):  # r for row
            if self.is_inconsistent_row(r):
                return True
        
        return False

    def row_echelon(self):
        result = self.copy_matrix()

        for r in range(result.size[0]):  # r for row
            lead = result.get_row(r)[0]

            if lead == 0 and r == 0:
                non_zero_lead_row = result.find_nonzero_lead(r + 1, 0)  # start searching from the second row
                
                if non_zero_lead_row == -1:
                    if result.is_inconsistent():
                        print("The system is inconsistent")
                        raise InconsistentSystemError
                    else:
                        print("The system has infinite number of solutions")
                        raise InfiniteSolutionsError
                
                result.swap_rows(r, non_zero_lead_row)
                result.divide(r, result.get_row(r)[0])
            
            if lead != 0:
                result.divide(r, result.get_row(r)[0])
            
            for prev in range(0, r):

                if lead != 0:
                    result.multiply(r, -1)
                    result.sum(r, prev)

                lead = result.get_row(r)[prev + 1]
                
                if lead == 0 and r == prev + 1:
                    non_zero_lead_row = result.find_nonzero_lead(r + 1, prev + 1)  # start searching from the second row
                    
                    if non_zero_lead_row == -1:
                        if result.is_inconsistent():
                            print("The system is inconsistent")
                            raise InconsistentSystemError
                        else:
                            print("The system has infinite number of solutions")
                            raise InfiniteSolutionsError
                    
                    result.swap_rows(r, non_zero_lead_row)
                
                    result.divide(r, result.get_row(r)[prev + 1])
                
                if lead != 0:
                    result.divide(r, result.get_row(r)[prev + 1])
        
        print("Finished converting to row echelon.\n")
        return result
    

    def reduced_row_echelon(self):
        result = self.copy_matrix()
        result = result.row_echelon()
        
        for r in range(result.size[0] - 2, -1, -1):
            for prev in range(r + 1, result.size[0]):
                result.multiply_then_sum(r, prev, -result.get_row(r)[prev])
        
        print("Finished converting to reduced row echelon.\n")
        return result
    

    def solve(self) -> list[float]:
        print("\n=============================\n")
        print("Attempting to solve the system:\n")
        result = self.reduced_row_echelon()

        solutions = []

        for i in range(self.size[0]):
            solutions.append(result.get_row(i)[-1])
        
        print("Solved!")
        return solutions
    
    def print_matrix_dbg(self):
        if print_matrix_dbg:
            print("\n")
            self.print()
            print("\n")