from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def main():
    model = cp_model.CpModel()

    # Task data: durations
    durations = [3, 2, 4, 3, 1,5,1,6,7,8,9,2,1]
    num_tasks = len(durations)
    num_machines = 4
    horizon = sum(durations)  # max possible end time

    all_tasks = []
    all_machines = range(num_machines)

    # Create variables
    for t in range(num_tasks):
        task = {}
        task['starts'] = []
        task['ends'] = []
        task['presences'] = []
        task['intervals'] = []
        for m in all_machines:
            start = model.new_int_var(0, horizon, f'start_t{t}_m{m}')
            end = model.new_int_var(0, horizon, f'end_t{t}_m{m}')
            presence = model.new_bool_var(f'presence_t{t}_m{m}')
            interval = model.new_optional_interval_var(start, durations[t], end, presence, f'interval_t{t}_m{m}')
            task['starts'].append(start)
            task['ends'].append(end)
            task['presences'].append(presence)
            task['intervals'].append(interval)
        all_tasks.append(task)

    # Each task is assigned to exactly one machine
    for t in range(num_tasks):
        model.add(sum(all_tasks[t]['presences']) == 1)

    # No overlap on each machine
    for m in all_machines:
        machine_intervals = []
        for t in range(num_tasks):
            machine_intervals.append(all_tasks[t]['intervals'][m])
        model.add_no_overlap(machine_intervals)

    # Minimize makespan (max end over all assigned tasks)
    ends = []
    for t in range(num_tasks):
        for m in all_machines:
            ends.append(all_tasks[t]['ends'][m])
    makespan = model.new_int_var(0, horizon, 'makespan')
    model.add_max_equality(makespan, ends)
    model.minimize(makespan)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Minimum makespan: {solver.value(makespan)}')

        assigned_tasks = [[] for _ in all_machines]

        for t in range(num_tasks):
            for m in all_machines:
                if solver.value(all_tasks[t]['presences'][m]):
                    s = solver.value(all_tasks[t]['starts'][m])
                    e = solver.value(all_tasks[t]['ends'][m])
                    assigned_tasks[m].append((t, s, e))
                    print(f'Task {t} assigned to machine {m}, starts at {s}, ends at {e}')

        # Plot the schedule
        plot_schedule(assigned_tasks, num_machines)

    else:
        print('No solution found.')

def plot_schedule(assigned_tasks, num_machines):
    fig, ax = plt.subplots(figsize=(10, 3))
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
    
    for m in range(num_machines):
        y_pos = 15 - m * 7
        for task in assigned_tasks[m]:
            t, start, end = task
            duration = end - start
            rect = mpatches.Rectangle((start, y_pos), duration, 5, color=colors[t % len(colors)])
            ax.add_patch(rect)
            ax.text(start + duration / 2, y_pos + 2.5, f'T{t}', ha='center', va='center', color='white', fontsize=9)

        ax.text(-1, y_pos + 2.5, f'M{m}', ha='right', va='center', fontsize=10, fontweight='bold')

    max_time = max([end for machine in assigned_tasks for (_, _, end) in machine])
    ax.set_xlim(0, max_time + 1)
    ax.set_ylim(0, 20)
    ax.set_xlabel('Time')
    ax.set_yticks([])
    ax.set_title('Task Schedule on 2 Machines')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
