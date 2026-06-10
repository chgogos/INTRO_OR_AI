"""
Solves the integer linear program:
    Maximize 3x + 4y
    s.t. 2x + 3y <= 100
         x + 2y <= 50
         3x + 2y <= 80
         x, y >= 0 and integer
Exports the model to my_model.lp in the same directory as this script.
"""

import os
from ortools.linear_solver import pywraplp


def solve_lp():
    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        print("Solver not found.")
        return

    # Integer Variables
    x = solver.IntVar(0, solver.infinity(), "x")
    y = solver.IntVar(0, solver.infinity(), "y")

    # Constraints
    solver.Add(2 * x + 3 * y <= 100)
    solver.Add(x + 2 * y <= 50)
    solver.Add(3 * x + 2 * y <= 80)

    # Objective
    solver.Maximize(3 * x + 4 * y)

    # Export model to file in the same directory as this script
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    lp_path = os.path.join(script_dir, "my_model.lp")
    with open(lp_path, "w") as f:
        f.write(solver.ExportModelAsLpFormat(False))
    print(f"Model exported to {lp_path}")

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"x = {x.solution_value()}")
        print(f"y = {y.solution_value()}")
        print(f"Maximum value = {solver.Objective().Value()}")
    else:
        print("No optimal solution found.")


if __name__ == "__main__":
    solve_lp()
