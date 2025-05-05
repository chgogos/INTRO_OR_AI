from ortools.constraint_solver import pywrapcp


def solve(board_size):
    solver = pywrapcp.Solver("n-queens")

    # Variables: The array index is the column, and the value is the row.
    queens = [solver.IntVar(0, board_size - 1, f"x{i}") for i in range(board_size)]

    # All rows must be different.
    solver.Add(solver.AllDifferent(queens))

    # No two queens can be on the same diagonal.
    solver.Add(solver.AllDifferent([queens[i] + i for i in range(board_size)]))
    solver.Add(solver.AllDifferent([queens[i] - i for i in range(board_size)]))

    db = solver.Phase(queens, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

    solver.NewSearch(db)
    while solver.NextSolution():
        for i in range(board_size):
            for j in range(board_size):
                if queens[j].Value() == i:
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()
    solver.EndSearch()


if __name__ == "__main__":
    solve(8)
