from ortools.sat.python import cp_model

model = cp_model.CpModel()

s = model.new_int_var(1, 9, "S")  # cannot be 0
e = model.new_int_var(0, 9, "E")
n = model.new_int_var(0, 9, "N")
d = model.new_int_var(0, 9, "D")
m = model.new_int_var(1, 9, "M")  # cannot be 0
o = model.new_int_var(0, 9, "O")
r = model.new_int_var(0, 9, "R")
y = model.new_int_var(0, 9, "Y")

letters = [s, e, n, d, m, o, r, y]

model.add_all_different(letters)

# SEND + MORE = MONEY
send = 1000 * s + 100 * e + 10 * n + d
more = 1000 * m + 100 * o + 10 * r + e
money = 10000 * m + 1000 * o + 100 * n + 10 * e + y

model.add(send + more == money)

solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    print(f"S = {solver.value(s)}")
    print(f"E = {solver.value(e)}")
    print(f"N = {solver.value(n)}")
    print(f"D = {solver.value(d)}")
    print(f"M = {solver.value(m)}")
    print(f"O = {solver.value(o)}")
    print(f"R = {solver.value(r)}")
    print(f"Y = {solver.value(y)}")
    print()
    print(f"{solver.value(send)} + {solver.value(more)} = {solver.value(money)}")

