from ortools.sat.python import cp_model

model = cp_model.CpModel()

x = model.new_int_var(-100, 100, "x")
y = model.new_int_var(-100, 100, "y")

# examples of linear constraints
model.add(x + 4 * y >= 100)  # x + 4y >= 100
model.add(cp_model.LinearExpr.sum([x, y]) == 1)  # x + y == 1
model.add(cp_model.LinearExpr.weighted_sum([x, y], [10, -5]) <= 50)  # 10x - 5y <= 50
model.add_linear_constraint(linear_expr=2 * x + 3 * y, lb=-10, ub=20)
