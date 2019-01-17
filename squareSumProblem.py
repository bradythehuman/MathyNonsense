def get_relevant_squares(n):
    relevant_squares = []
    for i in range(2, n):
        if i ** 2 >= 2 * n:
            return relevant_squares
        else:
            relevant_squares.append(i ** 2)


def get_adjacency_list(n, relevant_squares):
    adjacency_list = [[] for i in range(n)]
    for i in range(0, n):
        for square in relevant_squares:
            if square - (i + 1) > 0 and square - (i + 1) <= n:
                adjacency_list[i].append(square - (i + 1))
    return adjacency_list


def get_valid_paths(start, n, adjacency_list):
    valid_paths = []
    queue = [[start]]
    while queue:
        current = queue.pop(0)
        if len(current) == n:
            valid_paths.append(current)
        else:
            for adjacent in adjacency_list[current[-1] - 1]:
                if adjacent not in current:
                    queue.append(current + [adjacent])
    return valid_paths


if __name__ == "__main__":
    n = 15
    relevant_squares = get_relevant_squares(n)
    adjacency_list = get_adjacency_list(n, relevant_squares)
    valid_paths = []
    for i in range(n):
        valid_paths += get_valid_paths(i+1, n, adjacency_list)
    print(valid_paths)

