from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._vars = vars
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        for v in self._vars:
            print(f"{v}={self.value(v)}", end=" ")
        print()


model = cp_model.CpModel()
x = model.new_int_var(0, 4, "x")
y = model.new_int_var(0, 4, "y")
z = model.new_int_var(0, 4, "z")
model.add_all_different([x, y, z])
model.add(x + y + z == 6)

solver = cp_model.CpSolver()
solution_printer = SolutionPrinter([x, y, z])
solver.parameters.enumerate_all_solutions = True  # Enumerate all solutions.
solver.solve(model, solution_printer)
print(f"Number of solutions found {solution_printer.solution_count}")

