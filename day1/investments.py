from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x_A = solver.NumVar(200_000, 1_000_000, 'x_A')
x_B = solver.NumVar(200_000, 1_000_000, 'x_B')
x_C = solver.NumVar(200_000, 1_000_000, 'x_C')
x_D = solver.NumVar(200_000, 1_000_000, 'x_D')

# Constraints
solver.Add(x_A + x_B + x_C + x_D == 2_000_000)

solver.Add(x_A + x_B <= 1_500_000)

# Objective
solver.Maximize(0.09 * x_A + 0.11 * x_B + 0.05 * x_C + 0.08 * x_D)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f'Optimal solution found:')
    print(f'x_A = {x_A.solution_value():,.2f}')
    print(f'x_B = {x_B.solution_value():,.2f}')
    print(f'x_C = {x_C.solution_value():,.2f}')
    print(f'x_D = {x_D.solution_value():,.2f}')
    print(f'Maximum Return = {solver.Objective().Value():,.2f}')
else:
    print('The problem does not have an optimal solution.')
