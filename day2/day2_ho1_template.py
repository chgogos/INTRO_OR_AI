import os
from ortools.sat.python import cp_model


def main(costs):
    """
    costs is an N X N array
    costs[i][j] is the cost of assigning task i to employee j
    """
    N = len(costs)  # N = number of tasks (number of employees)

    # Create the model
    model = cp_model.CpModel()

    # Decision variables
    x = {}
    for i in range(N):  # i is the index for tasks
        for j in range(N):  # j i sthe index for employees
            x[i, j] = model.new_bool_var(f"x{i}_{j}")

    # Constraint1: Each task is assigned to exactly 1 employee
    for i in range(N):
        model.add(cp_model.LinearExpr.sum([x[i, j] for j in range(N)]) == 1)

    # Constraint2: Each employee is assigned to exactly 1 task
    # Fill here the missing part (1/2)

    # Objective
    vars = []
    weights = []
    for i in range(N):
        for j in range(N):
            vars.append(x[i, j])
            weights.append(costs[i][j])
    objective = cp_model.LinearExpr.weighted_sum(vars, weights)
    model.minimize(objective)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Display solution
    # Fill here the missing part (2/2)


def read_data(input_file):
    costs = []
    cost_line = []
    first_line = True
    with open(input_file, "r") as f:
        for line in f:
            if line[0] == "#" or line.strip() == "":
                continue
            if first_line:
                number_of_tasks = int(line)
                first_line = False
                continue
            for x in line.split():
                cost_line.append(int(x))
                if len(cost_line) == number_of_tasks:
                    costs.append(cost_line)
                    cost_line = []
    return costs


if __name__ == "__main__":
    fn = os.path.join(os.path.dirname(__file__), "assign10.txt")
    costs = read_data(fn)
    main(costs)
