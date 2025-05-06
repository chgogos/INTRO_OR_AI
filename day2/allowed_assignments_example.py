from ortools.sat.python import cp_model

model = cp_model.CpModel()
x_employee_1 = model.new_bool_var("x_employee_1")
x_employee_2 = model.new_bool_var("x_employee_2")
x_employee_3 = model.new_bool_var("x_employee_3")
x_employee_4 = model.new_bool_var("x_employee_4")

# Define the allowed assignments
allowed_assignments = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
]

model.add_allowed_assignments(
    [x_employee_1, x_employee_2, x_employee_3, x_employee_4], allowed_assignments
)

solver = cp_model.CpSolver()
solver.solve(model)

for var in [x_employee_1, x_employee_2, x_employee_3, x_employee_4]:
    print(f"{var.Name()}={solver.Value(var)}")

# x_employee_1=0
# x_employee_2=1
# x_employee_3=0
# x_employee_4=1
