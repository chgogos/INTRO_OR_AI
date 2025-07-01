from ortools.sat.python import cp_model

model = cp_model.CpModel()

t = model.new_int_var(1, 9, "T")  # cannot be 0
w = model.new_int_var(0, 9, "W")
o = model.new_int_var(0, 9, "O")
f = model.new_int_var(1, 9, "F")  # cannot be 0
u = model.new_int_var(0, 9, "U")
r = model.new_int_var(0, 9, "R")

letters = [t, w, o, f, u, r]

model.add_all_different(letters)

# TWO + TWO = FOUR
two = 100 * t + 10 * w + o
four = 1000 * f + 100 * o + 10 * u + r

model.add(two + two == four)

solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    print(f"T = {solver.value(t)}")
    print(f"W = {solver.value(w)}")
    print(f"O = {solver.value(o)}")
    print(f"F = {solver.value(f)}")
    print(f"U = {solver.value(u)}")
    print(f"R = {solver.value(r)}")
    print()
    print(f"{solver.value(two)} + {solver.value(two)} = {solver.value(four)}")
