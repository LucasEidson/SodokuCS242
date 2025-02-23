"""Takes some partial NxN soduku board and returns a solution"""

import math
import copy

N = 9  # N is a perfect square representing the dimensions of the board.


def main():
    board, unsolved = get_board_input()  # INDEXED BOARD[ROW][COL]
    propogate_constraints(board, unsolved)
    print("Finished Propgating Constraints, Result:")
    print_board(board)
    unsolved = get_unsolved(board)
    if unsolved:
        print("Backtracking...")
        backtrack_result = backtrack(board)
        if backtrack_result != "FAILURE":
            print("Board Solved!")
            print_board(backtrack_result)
        else:
            print("No Solution.")
    else:
        print("Board Solved!")
        print_board(board)


def backtrack(board):
    cur_unit = get_unsolved_unit(board)
    if cur_unit == None:
        return board
    for possible_val in cur_unit.domain:
        new_board = copy.deepcopy(board)
        new_unit = Unit(cur_unit.row, cur_unit.col, possible_val)
        new_board[cur_unit.row][cur_unit.col] = new_unit
        if check_consistency(new_unit, new_board):
            print_board(new_board)
            propogate_constraints(new_board, [new_unit])
            result = backtrack(new_board)
            if result != "FAILURE":
                return result
    return "FAILURE"


def get_unsolved_unit(board):
    """Returns an unsolved Unit with the smallest domain or nothing."""
    min_domain_size = N + 1
    best_unit = None
    for i in range(N):
        for j in range(N):
            if board[i][j].value == 0:
                if len(board[i][j].domain) < min_domain_size:
                    best_unit = board[i][j]
                    min_domain_size = len(best_unit.domain)
    return best_unit


def check_consistency(u, board):
    neighbors = get_neighbors(u, board)
    if u.value == 0 or len(u.domain) == 0:
        return False
    for neighbor in neighbors:
        if neighbor.value == u.value:
            return False
    return True


def get_unsolved(board):
    """returns a list of all unsolved units in board."""
    unsolved = []
    for i in range(N):
        for j in range(N):
            if board[i][j].value == 0:
                unsolved.append(board[i][j])
    return unsolved


def propogate_constraints(board, unsolved):
    """Checks consistency between each unit"""
    units = []
    for u in unsolved:
        units.append(u)
    unsolved = []
    while units:
        u = units.pop()
        if get_domain(u, board):
            units.extend(get_neighbors(u, board))


def get_domain(u, board):  # Constraint Propogation
    """Check constraints on Unit u and change domain accordingly, return True if domain is changed or False if it is not."""
    domain = u.domain.copy()
    if len(domain) == 1:
        u.value = domain[0]
        return True
    subgrid_row, subgrid_col = u.get_subgrid_index()
    subgrid_N = int(math.sqrt(N))
    subgrid_row *= subgrid_N
    subgrid_col *= subgrid_N  # These now represent the top left index of the subgrid
    unaccounted_row = list(range(1, N))
    unaccounted_col = list(range(1, N))
    unaccounted_grid = list(range(1, N))
    neighbors = get_neighbors(u, board)
    for nb in neighbors:
        val = nb.value
        if val in domain:
            domain.remove(val)
        if nb.row == u.row:
            if val in unaccounted_row:
                unaccounted_row.remove(val)
        elif nb.col == u.col:
            if val in unaccounted_col:
                unaccounted_col.remove(val)
        if (
            nb.row >= subgrid_row
            and nb.row < subgrid_row + subgrid_N
            and nb.col >= subgrid_col
            and nb.col < subgrid_col + subgrid_N
        ):
            if val in unaccounted_grid:
                unaccounted_grid.remove(val)
    revised = u.domain != domain
    u.domain = domain
    if len(u.domain) == 1:
        u.value = u.domain[0]
    return revised


def get_neighbors(u, board):
    """Returns each other unit which has a binary constraint with Unit u."""
    neighbors = []
    subgrid_row, subgrid_col = u.get_subgrid_index()
    subgrid_N = int(math.sqrt(N))
    for i in range(subgrid_N):
        subgrid_unit_row = (subgrid_row * subgrid_N) + i
        if subgrid_unit_row == u.row:
            continue
        for j in range(subgrid_N):
            subgrid_unit_col = (subgrid_col * subgrid_N) + j
            if subgrid_unit_col != u.col:
                neighbors.append(board[subgrid_unit_row][subgrid_unit_col])
    for i in range(N):
        row_nb = board[u.row][i]
        col_nb = board[i][u.col]
        if i != u.col:
            neighbors.append(row_nb)
        if i != u.row:
            neighbors.append(col_nb)
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
    for i in range(N):
        for j in range(N):
            print(board[i][j].value, end=" ")
        print()
    for _ in range(2 * N - 1):
        print("-", end="")
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
