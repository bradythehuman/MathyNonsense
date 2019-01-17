def build_graph(n: int):
    squares = [x * x for x in range(1, n)]
    for x in range(1, n + 1):
        for square in squares:
            y = square - x
            if