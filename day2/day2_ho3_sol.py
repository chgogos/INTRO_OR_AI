import os
from ortools.sat.python import cp_model


class Problem:
    def __init__(self, number_of_products, number_of_subsets):
        self.number_of_products = number_of_products
        self.number_of_subsets = number_of_subsets
        self.subsets = []

    def add_subset(self, cost, subset):
        self.subsets.append((cost, subset))
    
    def get_cost_of_subset(self, i):
        return self.subsets[i][0]
    
    def display_info(self):
        assert self.number_of_subsets == len(self.subsets)
        print(f"# products = {self.number_of_products}")
        print(f"# subsets = {self.number_of_subsets}")


def read_problem_data(fn):
    with open(fn, "r") as f:
        file_section = "A"
        for line in f:
            if line[0] == "#":
                continue
            if line.strip() == "":
                continue
            if file_section == "A":
                number_of_products, number_of_subsets = line.split()
                a_problem = Problem(int(number_of_products), int(number_of_subsets))
                file_section = "B"
                continue
            if file_section == "B":
                v = line.split()
                a_problem.add_subset(int(v[0]), [int(x) for x in v[2:]])
    return a_problem


def solve(a_problem):
    # Create model
    model = cp_model.CpModel()

    # decision variables
    x = {}
    for i in range(a_problem.number_of_subsets):
        x[i] = model.new_bool_var(f"x_{i}")

    # constraint: each product must be covered by exactly one of the subsets
    for j in range(a_problem.number_of_products):
        xs = []
        for i, (_, products) in enumerate(a_problem.subsets):
            if j + 1 in products:
                xs.append(x[i])
        if len(xs) == 0:
            print(f'empty xs for product {j+1}')
            exit(0)
        model.add(sum(xs) == 1)

    # objective
    obj = sum(
        x[i] * a_problem.get_cost_of_subset(i) for i in range(a_problem.number_of_subsets)
    )
    model.minimize(obj)

    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"status: {solver.status_name(status)}")
        print(f"obj={int(solver.objective_value):,}")
        print(f"time={solver.WallTime():.1f}")
        for i in range(a_problem.number_of_subsets):
            if solver.value(x[i]) == 1:
                print(f"Selected subset {i} : {a_problem.subsets[i]}")
    else:
        print("No solution found.")
        print(f"Status: {solver.StatusName(status)}")


if __name__ == "__main__":
    fn = os.path.join(os.path.dirname(__file__), "sp_135_51975.txt")
    a_problem = read_problem_data(fn)
    a_problem.display_info()
    solve(a_problem)