import numpy as np
import matplotlib.pyplot as plt
from ortools.sat.python import cp_model


def plot_points(locations):
    plt.figure(figsize=(6, 6))
    plt.scatter(locations[:, 0], locations[:, 1], c="red")
    for idx, (x, y) in enumerate(locations):
        plt.text(x + 0.2, y + 0.2, str(idx), fontsize=10)
    plt.title("Random TSP Locations")
    plt.grid(True)
    plt.show()


def plot_points_tour(locations, tour_of_vertices):
    plt.figure(figsize=(8, 6))
    for i in range(len(tour_of_vertices) - 1):
        start = locations[tour_of_vertices[i]]
        end = locations[tour_of_vertices[i + 1]]
        plt.plot([start[0], end[0]], [start[1], end[1]], "bo-")
    plt.scatter(locations[:, 0], locations[:, 1], c="red")
    for idx, (x, y) in enumerate(locations):
        plt.text(x + 0.2, y + 0.2, str(idx), fontsize=10)
    plt.title("TSP Route")
    plt.grid(True)
    plt.show()


def compute_euclidean_distance_matrix(locations):
    size = len(locations)
    distance_matrix = {}
    for from_node in range(size):
        distance_matrix[from_node] = {}
        for to_node in range(size):
            if from_node == to_node:
                distance_matrix[from_node][to_node] = 0
            else:
                # Compute Euclidean distance
                distance_matrix[from_node][to_node] = np.linalg.norm(
                    locations[from_node] - locations[to_node]
                )

    return distance_matrix


def tour_of_edges_to_tour_of_vertices(edges):
    successor = {u: v for u, v in edges}
    start = edges[0][0]
    tour = [start]
    while True:
        next_node = successor[tour[-1]]
        if next_node == start:  # If tour completed (cycle)
            break
        tour.append(next_node)
    tour.append(start)
    return tour


def display_distance_matrix(distance_matrix):
    num_locations = len(display_distance_matrix)
    for i in range(num_locations):
        for j in range(num_locations):
            print(f"{distance_matrix[i][j]:3d}", end=" ")
        print()


def create_graph(num_locations):
    # Generate random 2D points between (0,0) and (10,10)
    locations = np.random.uniform(0, 10, size=(num_locations, 2))
    distance_matrix = compute_euclidean_distance_matrix(locations)
    return locations, distance_matrix


def main(num_locations):
    locations, distance_matrix = create_graph(num_locations)
    plot_points(locations)

    # Create model
    model = cp_model.CpModel()

    # Create edge variables
    edge_vars = {}
    for u in range(num_locations):
        for v in range(num_locations):
            if u != v:
                edge_vars[u, v] = model.new_bool_var(f"e_{u}_{v}")

    # Associate edge_vars with edges using add_circuit
    # fmt: off
    circuit = [
        (u, v, var) #  (source, destination, variable)
        for (u, v), var in edge_vars.items()  
    ]
    # fmt: on
    model.add_circuit(circuit)

    # Objective: minimize the total cost of edges
    obj = sum(distance_matrix[u][v] * x for (u, v), x in edge_vars.items())
    model.minimize(obj)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    solver.parameters.log_search_progress = True
    status = solver.solve(model)

    # Print & plot solution
    if status == cp_model.OPTIMAL:
        tour_of_edges = [(u, v) for (u, v), x in edge_vars.items() if solver.value(x)]
        tour_of_vertices = tour_of_edges_to_tour_of_vertices(tour_of_edges)
        print("Optimal tour is", tour_of_vertices)
        print("The cost of the tour is: ", solver.objective_value)
        plot_points_tour(locations, tour_of_vertices)
    elif status == cp_model.FEASIBLE:
        tour_of_edges = [(u, v) for (u, v), x in edge_vars.items() if solver.value(x)]
        tour_of_vertices = tour_of_edges_to_tour_of_vertices(tour_of_edges)
        print("Feasible tour is: ", tour_of_vertices)
        print("The cost of the tour is: ", solver.objective_value)
        print("The lower bound of the tour is: ", solver.best_objective_bound)
        plot_points_tour(locations, tour_of_vertices)
    else:
        print("No solution found.")


if __name__ == "__main__":
    np.random.seed(42)  # fix seed for reproducibility
    main(num_locations=50)
