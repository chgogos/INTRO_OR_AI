from ortools.linear_solver import pywraplp
weights = [4, 7, 5, 3, 6, 2]
values = [10, 18, 12, 8, 14, 6]
capacities = [15, 12]
n = len(weights)        # number of items
m = len(capacities)     # number of knapsacks
# Create solver
solver = pywraplp.Solver.CreateSolver("SCIP")
# Decision variables
x = {} # x[i][k] = 1 if item i is placed in knapsack k, 0 otherwise
for i in range(n):
    for k in range(m):
        x[i, k] = solver.BoolVar(f"x_{i+1}_{k+1}")
# Objective: maximize total value
solver.Maximize(
    sum(values[i] * x[i, k] for i in range(n) for k in range(m))
)
# Capacity constraints
for k in range(m):
    solver.Add(
        sum(weights[i] * x[i, k] for i in range(n)) <= capacities[k]
    )
# Each item can be selected at most once
for i in range(n):
    solver.Add(
        sum(x[i, k] for k in range(m)) <= 1
    )
# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal objective value: {solver.Objective().Value()}")
    for k in range(m):
        print(f"\nKnapsack {k + 1}")
        total_weight = 0
        total_value = 0
        for i in range(n):
            if x[i, k].solution_value() > 0.5:
                print(
                    f"  Item {i + 1}: "
                    f"weight = {weights[i]}, value = {values[i]}"
                )
                total_weight += weights[i]
                total_value += values[i]
        print(f"  Total weight: {total_weight}")
        print(f"  Total value: {total_value}")
else:
    print("No optimal solution found.")
