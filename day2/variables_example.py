from ortools.sat.python import cp_model

model = cp_model.CpModel()

x = model.new_int_var(-10, 10, "x")
y = model.new_bool_var("y")
z = ~y  # only the new_xxx_var variables get names

domain1 = cp_model.Domain.from_values([2, 5, 8, 10, 20, 50, 90])
domain2 = cp_model.Domain.from_intervals([[8, 12], [14, 20]])
w = model.new_int_var_from_domain(domain1.union_with(domain2), "w")

for var in [x, y, w]:
    print(f"{var.Name()} has domain {var.Proto().domain}")


