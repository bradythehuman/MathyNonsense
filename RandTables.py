from random import randint
import math

row_totals = []  # gives totals that must be matched by rand values
col_totals = []


def rand_exp_table(max_value, row_count):
    exp_table = [[], []]
    for i in range(row_count):
        exp_table[0].append(randint(0, max_value))
        exp_table[1].append(randint(0, max_value))
    return exp_table


def sum_margins(exp_table):
    row_totals.clear()
    col_totals.clear()
    for i in range(len(exp_table[0])):
        row_totals.append(exp_table[0][i] + exp_table[1][i])
    col_totals.append(sum(exp_table[0]))
    col_totals.append(sum(exp_table[1]))


# splits row total list in half, assigns random
def distribute(sub_col_total, sub_row_totals, col_a_rand):
    if len(sub_row_totals) == 1:
        col_a_rand.append(sub_col_total)
    else:
        splice = int(len(sub_row_totals) / 2)
        top = sub_row_totals[:splice]
        bottom = sub_row_totals[splice:]
        top_total = sum(top)
        bottom_total = sum(bottom)
        rand_for_smaller = randint(max(0, sub_col_total - max(top_total, bottom_total)),
                                   min(sub_col_total, min(top_total, bottom_total)))
        if top_total < bottom_total:  # top_is_smaller
            rand_for_top = rand_for_smaller
            rand_for_bottom = sub_col_total - rand_for_smaller
        else:
            rand_for_top = sub_col_total - rand_for_smaller
            rand_for_bottom = rand_for_smaller
        distribute(rand_for_top, top, col_a_rand)
        distribute(rand_for_bottom, bottom, col_a_rand)


def increment(col_total, row_totals, col_a_rand):
    rows = []
    for i in range(96):
        if row_totals[i] != 0:
            rows.append(i)
            col_a_rand.append(0)
    for i in range(col_total):
        j = rows[randint(0, len(rows)-1)]
        col_a_rand[j] += 1
        if col_a_rand[j] == row_totals[j]:
            rows.remove(j)


def get_tables(table_count, exp_table):
    sum_margins(exp_table)
    tables = []
    for i in range(table_count):
        col_a_rand = []
        increment(col_totals[0], row_totals, col_a_rand)
        col_b_rand = []
        for i in range(0, len(exp_table[0])):
            col_b_rand.append(row_totals[i] - col_a_rand[i])
        tables.append((col_a_rand[:], col_b_rand[:]))
    return tables


def get_table2(col_totals, row_totals):
    table = [[], []]
    rows = []
    for i in range(96):
        if row_totals[i] != 0:
            rows.append((0, i))
            rows.append((1, i))
        table[0].append(0)
        table[1].append(0)
    col_counts = [col_totals[0], col_totals[1]]
    while rows:
        cell = rows[randint(0, len(rows)-1)]
        table[cell[0]][cell[1]] += 1
        if table[0][cell[1]] + table[1][cell[1]] == row_totals[cell[1]]:
            if col_counts[0]:
                rows.remove((0, cell[1]))
            if col_counts[1]:
                rows.remove((1, cell[1]))
        col_counts[cell[0]] -= 1
        if not col_counts[cell[0]]:
            for cell2 in rows:
                if cell2[0] == cell[0]:
                    rows.remove(cell2)
    return table


def get_tables2(table_count, exp_table):
    sum_margins(exp_table)
    tables = []
    for i in range(table_count):
        print(i)
        tables.append(get_table2(col_totals, row_totals))
    return tables


def logfac(x):
    return math.log(math.factorial(x))


def get_p(cols, numerator, t):
    denomenator = t
    for col in cols:
        for cell in col:
            denomenator += logfac(cell)
    return numerator - denomenator


def get_all_p(tables, exp_table):
    marginal_fac = 0
    for t in row_totals + col_totals:
        marginal_fac += logfac(t)
    total_fac = logfac(col_totals[0] + col_totals[1])

    exp_p = get_p(exp_table, marginal_fac, total_fac)
    p_values = []
    for table in tables:
        p_values.append(get_p(table, marginal_fac, total_fac))

    sort = [0, 0]
    for p_value in p_values:
        if p_value > exp_p:
            sort[0] += 1
        else:
            sort[1] += 1

    print(p_values)
    print(exp_p)
    print("above: " + str(sort[0]) + "   bellow: " + str(sort[1]))


if __name__ == "__main__":
    main_table = rand_exp_table(300, 96)  # Nested list cols then rows
    rand_tables = get_tables2(1000, main_table)  # This is where all the tables are stored as tuples of the form (col_a, col_b)
    print(rand_tables)

    # get_all_p(rand_tables, main_table)
