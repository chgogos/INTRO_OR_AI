from ortools.sat.python import cp_model

model = cp_model.CpModel()

# A value representing the load that needs to be transported
load_value = model.new_int_var(0, 100, "load_value")

# A variable to decide which truck to rent
truck_a = model.new_bool_var("truck_a")
truck_b = model.new_bool_var("truck_b")
truck_c = model.new_bool_var("truck_c")

# Rent at least one truck
model.add_at_least_one([truck_a, truck_b, truck_c])

# Depending on which truck is rented, the load value is limited
model.add(load_value <= 50).only_enforce_if(truck_a)
model.add(load_value <= 80).only_enforce_if(truck_b)
model.add(load_value <= 100).only_enforce_if(truck_c)

# some logic determined the load value to be ... 75
model.add(load_value == 75)

# Minimize the rent cost
model.minimize(30 * truck_a + 40 * truck_b + 80 * truck_c)

solver = cp_model.CpSolver()
solver.solve(model)

print(solver.Value(truck_a), solver.Value(truck_b), solver.Value(truck_c))  # 0 1 0
