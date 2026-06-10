from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SCIP")

# Binary Decision Variables
x = []
for i in range(5):
    x.append(solver.IntVar(0, 1, f"x{i+1}"))

# Objective function
solver.Maximize(4 * x[0] + 2 * x[1] + x[2] + 2 * x[3] + 10 * x[4])

# Constraint
solver.Add(12 * x[0] + x[1] + x[2] + 2 * x[3] + 4 * x[4] <= 15)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Solution:")
    for i in range(5):
        print(f"x{i+1} = {int(x[i].solution_value())}")
    print(f"Maximum objective value = {solver.Objective().Value()}")
else:
    print("No optimal solution found.")


