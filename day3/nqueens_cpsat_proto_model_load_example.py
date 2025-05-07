from ortools.sat.python import cp_model
from pathlib import Path
import os


def solve():
    # Create the solver
    model = cp_model.CpModel()

    # Load model proto file.
    filename = os.path.join(os.path.dirname(__file__), "nqueens_cpsat_proto_model.pb")
    model.Proto().ParseFromString(Path(filename).read_bytes())
    print("Model proto file loaded!")

    # Solve the model.
    solver = cp_model.CpSolver()
    solver.solve(model)

    # Display proto file of the solution.
    print("\nProto solution")
    solution_proto = solver.ResponseProto()
    print(solution_proto)


if __name__ == "__main__":
    solve()
