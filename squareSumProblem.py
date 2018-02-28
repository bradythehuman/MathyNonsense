n = 15
relevant_squares = []
for i in range(2, n):
    if i ** 2 >= 2 * n:
        break
    else:
        relevant_squares.append(i**2)
print(relevant_squares)
