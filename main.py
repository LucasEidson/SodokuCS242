"""Takes some partial NxN soduku board and returns a solution"""

import math
import queue


N = 9  # N is a perfect square representing the dimensions of the board.


def main():
    board, unsolved = get_board_input()  # INDEXED BOARD[ROW][COL]
    propogate_constraints(board, unsolved)
    print_board(board)


def propogate_constraints(board, unsolved):
    """Checks consistency between each unit"""
    units = []
    for u in unsolved:
        units.append(u)
    while units:
        u = units.pop()
        if get_domain(u, board):
            units.extend(get_neighbors(u, board))


def get_domain(u, board):  # Constraint Propogation
    """Check constraints on Unit u and change domain accordingly, return True if domain is changed or False if it is not."""
    domain = u.domain.copy()
    if len(domain) == 1:
        u.value = domain[0]
        return False

    # Check row and column:
    unaccounted_row = list(range(1, N))
    unaccounted_col = list(range(1, N))
    for i in range(N):
        if i != u.row:
            column_unit = board[i][u.col]
            for value in column_unit.domain:
                if value in unaccounted_col:
                    unaccounted_col.remove(value)
            if column_unit.value in domain:
                domain.remove(column_unit.value)
        if i != u.col:
            row_unit = board[u.row][i]
            for value in row_unit.domain:
                if value in unaccounted_row:
                    unaccounted_row.remove(value)
            if row_unit.value in domain:
                domain.remove(row_unit.value)
    if len(unaccounted_row) == 1:
        domain = [unaccounted_row[0]]
    elif len(unaccounted_col) == 1:
        domain = [unaccounted_col[0]]
    else:
        # Check subgrid:
        unaccounted_grid = list(range(1, N))
        subgrid_row, subgrid_col = u.get_subgrid_index()
        subgrid_N = int(math.sqrt(N))
        for i in range(subgrid_N):
            for j in range(subgrid_N):
                if i == u.row and j == u.col:
                    continue
                subgrid_unit = board[(subgrid_row * subgrid_N) + i][
                    (subgrid_col * subgrid_N) + j
                ]
                for value in subgrid_unit.domain:
                    if value in unaccounted_grid:
                        unaccounted_grid.remove(value)
                if subgrid_unit.value in domain:
                    domain.remove(subgrid_unit.value)
        if len(unaccounted_grid) == 1:
            domain = [unaccounted_grid[0]]

    revised = u.domain != domain
    u.domain = domain
    if len(u.domain) == 1:
        u.value = u.domain[0]
    return revised


def get_neighbors(u, board):
    """Returns each other unit which has a binary constraint with Unit u."""
    neighbors = []
    for i in range(N):
        if i != u.row:
            neighbors.append(board[i][u.col])
        if i != u.col:
            neighbors.append(board[u.row][i])
        for j in range(N):
            if i != u.row and j != u.col:
                neighbors.append(board[i][j])
    return neighbors


def get_board_input():
    """Return 2D Board List and list of unsolved unit objects created from stdin"""
    board = []
    unsolved = []
    for i in range(N):
        board.append([])
        line = input()
        line = line.split()
        for j in range(N):
            val = int(line[j])
            new_unit = Unit(i, j, val)
            if val == 0:
                unsolved.append(new_unit)
            board[i].append(new_unit)
    return board, unsolved


def print_board(board):
    print("PRINTING BOARD: ")
    for i in range(N):
        for j in range(N):
            print(board[i][j].value, end=" ")
        print()


class Unit:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.domain = list(range(1, N + 1)) if value == 0 else [value]
        self.value = value

    def get_subgrid_index(self):
        """Returns the index (x, y) of the subgrid of the Variable where an NxN matrix has N sqrt(N)xsqrt(N) subgrids"""
        subgrid_row = math.floor(self.row / (math.sqrt(N)))
        subgrid_col = math.floor(self.col / (math.sqrt(N)))
        return (subgrid_row, subgrid_col)


if __name__ == "__main__":
    main()
