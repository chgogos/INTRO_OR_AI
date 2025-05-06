from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.new_int_var(-100, 100, "x")
y = model.new_int_var(-100, 100, "y")
z = model.new_int_var(-100, 100, "z")

# Adding an all-different constraint
model.add_all_different([x, y, z])

solver = cp_model.CpSolver()
status = solver.solve(model)

# fmt:off
print(f"x={solver.Value(x)}, y={solver.Value(y)}, z={solver.Value(z)}") # x=-100, y=-99, z=-98
