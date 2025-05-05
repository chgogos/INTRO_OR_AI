from ortools.sat.python import cp_model


def solve(board_size):
    # Create the solver
    model = cp_model.CpModel()

    # Variables: The array index is the column, and the value is the row.
    queens = [model.new_int_var(0, board_size - 1, f"x{i}") for i in range(board_size)]

    # All rows must be different.
    model.add_all_different(queens)

    # No two queens can be on the same diagonal.
    model.add_all_different([queens[i] + i for i in range(board_size)])
    model.add_all_different([queens[i] - i for i in range(board_size)])

    # Solve the model.
    solver = cp_model.CpSolver()
    solver.solve(model)

    # Display the first solution found and terminate.
    all_queens = range(board_size)
    for i in all_queens:
        for j in all_queens:
            if solver.value(queens[j]) == i:
                # There is a queen in column j, row i.
                print("Q", end=" ")
            else:
                print("_", end=" ")
        print()


if __name__ == "__main__":
    solve(8)

