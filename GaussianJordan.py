from fractions import Fraction


class LinearSys:
    def __init__(self):
        self.rows = int(input("How many equations? "))
        self.cols = int(input("How many variables? ")) + 1
        self.data = []  # Outer array for row, internal for col
        print("Enter rows in \"a1 a2 ... aN b\" format\n")
        for i in range(self.rows):
            row = input("Row " + str(i) + " > ").split(' ')
            for i in range(len(row)):
                row[i] = Fraction(int(row[i]), 1)
            self.data.append(row)

    # Pre : Data must contain at least a variable plus the constant
    def print_sys(self):
        max_spaces = []
        for i in range(self.cols):
            max = 0
            for j in range(self.rows):
                curr = len(str(self.data[j][i]))
                if curr > max:
                    max = curr
            max_spaces.append(max + 1)
        for row in self.data:
            print("[", end="")
            for i in range(len(row) - 1):
                curr = str(row[i])
                print((" " * (max_spaces[i] - len(curr))) + curr, end="")
            print(" |" + (" " * (max_spaces[-1] - len(str(row[-1])))) + str(row[-1]) + " ]")
        print()

    # Post: returns index of first non zero row at given collumn excluding those before the starting row
    def first_non_zero(self, col, start_row):
        for i in range(start_row, self.rows):
            if self.data[col][i] != 0:
                return i
        return -1

    def swap(self, row_index1, row_index2):
        row1 = self.data[row_index1]
        row2 = self.data[row_index2]
        self.data[row_index1] = row2
        self.data[row_index2] = row1

    def multiply(self, scalar, row_index):
        for i in range(self.cols):
            self.data[row_index][i] = self.data[row_index][i] * scalar

    def add(self, effected_row, effector_row, scalar):
        for i in range(self.cols):
            self.data[effected_row][i] = self.data[effected_row][i] + (scalar * self.data[effector_row][i])

    def cancel_by_add(self, effected_row, effector_row, col):
        self.add(effected_row, effector_row, -self.data[effected_row][col])

    def isolate_pivot(self, pivot_row, col):
        for i in range(0, pivot_row):
            self.cancel_by_add(i, pivot_row, col)
        for i in range(pivot_row + 1, self.rows):
            self.cancel_by_add(i, pivot_row, col)

    def gaussian_jordan(self):
        fixed_rows = 0
        for i in range(self.cols - 1):
            curr_index = self.first_non_zero(i, fixed_rows)
            if curr_index != -1:
                self.swap(fixed_rows, curr_index)
                print("swap")
                system.print_sys()
                self.multiply(Fraction(1, self.data[fixed_rows][i]), fixed_rows)
                print("multiply")
                system.print_sys()
                self.isolate_pivot(fixed_rows, i)
                print("add")
                system.print_sys()
                fixed_rows += 1

    def back_sub(self):
        pass


if __name__ == "__main__":
    system = LinearSys()
    print()
    system.print_sys()
    system.gaussian_jordan()
