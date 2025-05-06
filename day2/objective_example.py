from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Decision variables
x = model.new_int_var(0, 5, "x")
y = model.new_int_var(0, 5, "y")

# Absolute value terms
abs_diff = model.new_int_var(0, 5, "abs_diff")
abs_sum_minus_5 = model.new_int_var(0, 5, "abs_sum_minus_5")

# Define abs terms
model.add_abs_equality(abs_diff, x - y)
model.add_abs_equality(abs_sum_minus_5, x + y - 5)

# Objective: minimize |x - y| + |x + y - 5|
model.minimize(abs_diff + abs_sum_minus_5)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"x = {solver.value(x)}, y = {solver.value(y)}")
    print(f"|x - y| = {solver.value(abs_diff)}")
    print(f"|x + y - 5| = {solver.value(abs_sum_minus_5)}")
    print(f"Objective value = {solver.objective_value}")
else:
    print("No solution found.")
