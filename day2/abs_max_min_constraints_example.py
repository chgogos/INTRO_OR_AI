from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.new_int_var(-100, 100, "x")
y = model.new_int_var(-100, 100, "y")
z = model.new_int_var(-100, 100, "z")

# Create an auxiliary variable for the absolute value of x+z
abs_xz = model.new_int_var(0, 200, "|x+z|")
model.add_abs_equality(target=abs_xz, expr=x + z)

# Create auxiliary variables to capture the maximum and minimum of x, (y-1), and z
max_xyz = model.new_int_var(0, 100, "max(x, y-1, z)")
model.add_max_equality(target=max_xyz, exprs=[x, y - 1, z])

min_xyz = model.new_int_var(-100, 100, "min(x, y-1, z)")
model.add_min_equality(target=min_xyz, exprs=[x, y - 1, z])

model.add(abs_xz + max_xyz == min_xyz)

solver = cp_model.CpSolver()
solver.solve(model)

# fmt:off
print(f"x={solver.Value(x)}, y={solver.Value(y)}, z={solver.Value(z)}") # x=0, y=-1, z=0
