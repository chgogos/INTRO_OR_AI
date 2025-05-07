import os
from collections import defaultdict
from ortools.linear_solver import pywraplp


class Problem:
    def __init__(self, number_of_warehouses, number_of_clients):
        self.number_of_warehouses = number_of_warehouses
        self.number_of_clients = number_of_clients
        self.warehouses = defaultdict()
        self.clients = defaultdict()

    def add_warehouse(self, warehouse_id, maximum_demand, fixed_cost):
        self.warehouses[warehouse_id] = (maximum_demand, fixed_cost)

    def add_demand_per_client(self, client_id, demand, costs_per_warehouse):
        self.clients[client_id] = (demand, costs_per_warehouse)

    def get_cost_per_unit_for(self, client_id, warehouse_id):
        return self.clients[client_id][1][warehouse_id]

    def get_fixed_cost_for(self, warehouse_id):
        return self.warehouses[warehouse_id][1]

    def get_maximum_demand_for(self, warehouse_id):
        return self.warehouses[warehouse_id][0]

    def get_client_demand(self, client_id):
        return self.clients[client_id][0]

    def display_info(self):
        print(f"Number of Warehouses = {self.number_of_warehouses}")
        for w, (md, fc) in self.warehouses.items():
            print(f"Warehouse = {w}, maximum demand = {md}, fixed cost = {fc}")
        print(f"Number of Clients = {self.number_of_clients}")
        for c, (d, cost_per_warehouse) in self.clients.items():
            print(
                f"Client = {c}, demand = {d}, cost per warehouse = {cost_per_warehouse}"
            )


def read_problem_data(fn):
    w = 0
    c = 0
    with open(fn, "r") as f:
        file_section = "A"
        for line in f:
            if line[0] == "#":
                continue
            if line.strip() == "":
                continue
            if file_section == "A":
                now, noc = line.split()
                a_problem = Problem(int(now), int(noc))
                file_section = "B"
                continue
            if file_section == "B" and w < a_problem.number_of_warehouses:
                md, fc = line.split()
                a_problem.add_warehouse(w, float(md), float(fc))
                w += 1
                continue
            if file_section == "B" and c < a_problem.number_of_clients:
                d = int(line)
                c += 1
                costs_per_warehouse = []
                file_section = "C"
                continue
            if file_section == "C":
                for y in line.split():
                    costs_per_warehouse.append(float(y) / d)
                if len(costs_per_warehouse) == a_problem.number_of_warehouses:
                    a_problem.add_demand_per_client(c, d, costs_per_warehouse)
                    file_section = "B"
    return a_problem


def solve(a_problem):
    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        return

    # decision variables
    x = defaultdict()  # quantity that client c gets from warehouse w
    for c in a_problem.clients:
        client_demand = a_problem.get_client_demand(c)
        for w in a_problem.warehouses:
            maximum_demand = a_problem.warehouses[w][0]
            # x[c, w] = solver.NumVar(0, min(client_demand, maximum_demand), f"x{c}_{w}")
            x[c, w] = solver.NumVar(0, solver.infinity(), f"x{c}_{w}")
    y = defaultdict()
    for w in a_problem.warehouses:
        y[w] = solver.BoolVar(f"y{w}")  # y_w is 1 when warehouse is used, 0 otherwise

    # constraint1: the demand of each client must be covered
    for c in a_problem.clients:
        client_demand = a_problem.clients[c][0]
        solver.Add(sum(x[c, w] for w in a_problem.warehouses) == client_demand)

    # constraint2: the total quantity that is drawn from each warehouse by all clients must be less than or equal to the warehouse's availability
    for w in a_problem.warehouses:
        maximum_demand = a_problem.warehouses[w][0]
        solver.Add(sum(x[c, w] for c in a_problem.clients) <= maximum_demand * y[w])

    # objective
    objective_terms_1 = []
    for c in a_problem.clients:
        for w in a_problem.warehouses:
            objective_terms_1.append(x[c, w] * a_problem.get_cost_per_unit_for(c, w))
    obj1 = solver.Sum(objective_terms_1)

    objective_terms_2 = []
    for w in a_problem.warehouses:
        objective_terms_2.append(y[w] * a_problem.get_fixed_cost_for(w))
    obj2 = solver.Sum(objective_terms_2)

    solver.Minimize(obj1 + obj2)

    # solve
    status = solver.Solve()

    # display results
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f"Costs = {obj1.solution_value():.1f}")
        print(f"Fixed costs = {obj2.solution_value():.1f}")
        print(f"Total cost = {solver.Objective().Value()}, STATUS = {status}")
        for w in a_problem.warehouses:
            if y[w].solution_value() == 0:
                print(f"Warehouse {w} is not used!\n")
                continue
            qty_shipped = 0
            cost_shipped = 0
            print(f"Warehouse = {w}")
            for c in a_problem.clients:
                if x[c, w].solution_value() > 0:
                    print(f"\tClient {c}, QTY = {x[c, w].solution_value():.1f}")
                    qty_shipped += x[c, w].solution_value()
                    cost_shipped += x[
                        c, w
                    ].solution_value() * a_problem.get_cost_per_unit_for(c, w)
            print(
                f"TOTAL QTY = {qty_shipped:.1f}/{a_problem.get_maximum_demand_for(w)}, TOTAL COST = {cost_shipped:.1f}\n"
            )

        # for w in a_problem.warehouses:
        #     print(f"y[{w}]={y[w].solution_value()}")


if __name__ == "__main__":
    fn = os.path.join(os.path.dirname(__file__), "w4_c8.txt")
    a_problem = read_problem_data(fn)
    solve(a_problem)