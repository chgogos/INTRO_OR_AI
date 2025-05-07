from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("CBC")

# Binary Decision Variables
# x = []
# for i in range(5):
#     x.append(solver.IntVar(0, 1, f"x{i+1}"))

x = [solver.IntVar(0,1,f"x{i+1}") for i in range(5)]

# Constraint
solver.Add(12 * x[0] + x[1] + x[2] + 2 * x[3] + 4 * x[4] <= 15)

# Objective function
# solver.Maximize(4 * x[0] + 2 * x[1] + x[2] + 2 * x[3] + 10 * x[4])
solver.Maximize(x[0] + x[1] + x[2] + x[3] + x[4])

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Solution:")
    for i in range(5):
        print(f"x{i+1} = {int(x[i].solution_value())}")
    print(f"Maximum objective value = {solver.Objective().Value()}")
else:
    print("No optimal solution found.")


