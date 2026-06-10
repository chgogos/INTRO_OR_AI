from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Data (costs, nutritional values)
c = [2, 1.5, 3, 2, 4]  # Cost per unit for each food
A = [
    [300, 200, 400, 250, 500],  # Calories
    [5, 10, 8, 6, 12],          # Protein
    [1, 2, 3, 2, 4]             # Vitamins
]
b = [1200, 50, 5]  # Minimum nutritional requirements

# Variables (continuous)
x = [solver.NumVar(0.0, solver.infinity(), f'x{i+1}') for i in range(5)]

# Objective function: Minimize c^T * x
objective = solver.Objective()
for i in range(5):
    objective.SetCoefficient(x[i], c[i])
objective.SetMinimization()

# Constraints: A * x >= b
for i in range(3):  # 3 constraints
    constraint = solver.Constraint(b[i], solver.infinity())
    for j in range(5):  # 5 foods
        constraint.SetCoefficient(x[j], A[i][j])

# Solve the problem
status = solver.Solve()

# Results
solution = {}
if status == pywraplp.Solver.OPTIMAL:
    solution = {
        'x': [x[i].solution_value() for i in range(5)],
        'objective': solver.Objective().Value()
    }

print(solution)
