SYMBOLS = "xyzwabcdefghijklmnopqrstuv"

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


    def print(self):
        for row in self._data:
            for col in row:
                print(f"{col} ", end="")
            print()
    

    def divide(self, row, num):
        for i in range(self.size[1]):
            self._data[row][i] = self.get_row(row)[i] / num


    def multiply(self, row, num):
        for i in range(self.size[1]):
            self._data[row][i] = self.get_row(row)[i] * num
    

    def sum(self, r1, r2):
        for i in range(self.size[1]):
            self._data[r1][i] += self.get_row(r2)[i]
    

    def multiply_then_sum(self, r1, r2, num):
        for i in range(self.size[1]):
            self._data[r1][i] += num * self.get_row(r2)[i]
        

    def get_row(self, row):
        return self._data[row]
        

    def copy(self):
        result = Mat(self.size)

        for row in self._data:
            result.add_row(row.copy())
        
        return result


    def row_echelon(self):
        result = self.copy()

        for i in range(result.size[0]):
            result.divide(i, result.get_row(i)[0])

        for j in range(0, i):
            result.multiply(i, -1)
            result.sum(i, j)
            result.divide(i, result.get_row(i)[j+1])
        
        return result
    

    def reduced_row_echelon(self):
        result = self.copy()
        result = result.row_echelon()
        
        for i in range(result.size[0]-2, -1, -1):
            for j in range(i+1, result.size[0]):
                result.multiply_then_sum(i, j, -result.get_row(i)[j])
        
        return result
    

    def solve(self):
        result = self.reduced_row_echelon()
        for i in range(self.size[0]):
            print(f"{SYMBOLS[i].upper()} = {result.get_row(i)[-1]}")
