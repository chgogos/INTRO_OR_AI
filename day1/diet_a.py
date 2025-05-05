from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Variables (continuous)
x1 = solver.NumVar(0.0, solver.infinity(), 'x1')
x2 = solver.NumVar(0.0, solver.infinity(), 'x2')
x3 = solver.NumVar(0.0, solver.infinity(), 'x3')
x4 = solver.NumVar(0.0, solver.infinity(), 'x4')
x5 = solver.NumVar(0.0, solver.infinity(), 'x5')

# Objective function
solver.Minimize(2 * x1 + 1.5 * x2 + 3 * x3 + 2 * x4 + 4 * x5)

# Constraints
solver.Add(300 * x1 + 200 * x2 + 400 * x3 + 250 * x4 + 500 * x5 >= 1200)  # Calories
solver.Add(5 * x1 + 10 * x2 + 8 * x3 + 6 * x4 + 12 * x5 >= 50)  # Protein
solver.Add(x1 + 2 * x2 + 3 * x3 + 2 * x4 + 4 * x5 >= 5)  # Vitamins

# Solve the problem
status = solver.Solve()

# Results
solution = {}
if status == pywraplp.Solver.OPTIMAL:
    solution = {
        'x1': x1.solution_value(),
        'x2': x2.solution_value(),
        'x3': x3.solution_value(),
        'x4': x4.solution_value(),
        'x5': x5.solution_value(),
        'objective': solver.Objective().Value()
    }

print(solution)

