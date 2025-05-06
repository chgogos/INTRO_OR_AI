from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.new_int_var(-100, 100, "x")
y = model.new_int_var(-100, 100, "y")
z = model.new_int_var(-100, 100, "z")

xyz = model.new_int_var(-(100**3), 100**3, "x*y*z")
model.add_multiplication_equality(xyz, [x, y, z])  # xyz = x*y*z

model.add_modulo_equality(x, y, 10)  # x = y % 10
model.add_division_equality(z, y, 2)  # z = y // 2

model.add(xyz >= 10)

solver = cp_model.CpSolver()
status = solver.solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"x={solver.Value(x)}, y={solver.Value(y)}, z={solver.Value(z)}") # x=1, y=11, z=5
else:
    print("No solution found")
    
    