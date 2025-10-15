from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("GLOP")

# Decision variables
x1 = solver.NumVar(0, solver.infinity(), "x1")
x2 = solver.NumVar(0, solver.infinity(), "x2")
x3 = solver.NumVar(0, solver.infinity(), "x3")
x4 = solver.NumVar(0, solver.infinity(), "x4")
x5 = solver.NumVar(0, solver.infinity(), "x5")
x6 = solver.NumVar(0, solver.infinity(), "x6")
x7 = solver.NumVar(0, solver.infinity(), "x7")

# Constraints
solver.Add(x1 + x4 + x5 + x6 + x7 >= 90)
solver.Add(x1 + x2 + x5 + x6 + x7 >= 80)
solver.Add(x1 + x2 + x3 + x6 + x7 >= 100)
solver.Add(x1 + x2 + x3 + x4 + x7 >= 60)
solver.Add(x1 + x2 + x3 + x4 + x5 >= 80)
solver.Add(x2 + x3 + x4 + x5 + x6 >= 150)
solver.Add(x3 + x4 + x5 + x6 + x7 >= 140)


# Objective
solver.Minimize(x1 + x2 + x3 + x4 + x5 + x6 + x7)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Optimal solution found:")
    print(f"x1 = {round(x1.solution_value())}")
    print(f"x2 = {round(x2.solution_value())}")
    print(f"x3 = {x3.solution_value()}")
    print(f"x4 = {x4.solution_value()}")
    print(f"x5 = {x5.solution_value()}")
    print(f"x6 = {x6.solution_value()}")
    print(f"x7 = {x7.solution_value()}")
    print(f"Total employees = {solver.Objective().Value()}")
    print(f"Δευτέρα = {x1.solution_value() + x4.solution_value() + x5.solution_value() + x6.solution_value() + x7.solution_value()}")
    print(f"Τρίτη = {x1.solution_value() + x2.solution_value() + x5.solution_value() + x6.solution_value() + x7.solution_value()}")
    print(f"Τετάρτη = {x1.solution_value() + x2.solution_value() + x3.solution_value() + x6.solution_value() + x7.solution_value()}")
    print(f"Πέμπτη = {x1.solution_value() + x2.solution_value() + x3.solution_value() + x4.solution_value() + x7.solution_value()}")
    print(f"Παρασκευή = {x1.solution_value() + x2.solution_value() + x3.solution_value() + x4.solution_value() + x5.solution_value()}")
    print(f"Σάββατο = {x2.solution_value() + x3.solution_value() + x4.solution_value() + x5.solution_value() + x6.solution_value()}")
    print(f"Κυριακή = {x3.solution_value() + x4.solution_value() + x5.solution_value() + x6.solution_value() + x7.solution_value()}")
    
else:
    print("The problem does not have an optimal solution.")
