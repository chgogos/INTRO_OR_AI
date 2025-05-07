from ortools.sat.python import cp_model

# Model
m = cp_model.CpModel()
durs = [3, 2, 4, 1]
horizon = sum(durs)

starts = [m.new_int_var(0, horizon, f's{i}') for i in range(4)]
ends = [m.new_int_var(0, horizon, f'e{i}') for i in range(4)]
intervals = [m.new_interval_var(starts[i], durs[i], ends[i], f'int{i}') for i in range(4)]

m.add_no_overlap(intervals)

# Precedence constraint: Task 0 must finish before Task 2 starts
m.add(ends[0] <= starts[2])

makespan = m.new_int_var(0, horizon, 'makespan')
m.add_max_equality(makespan, ends)
m.minimize(makespan)

# Solve
s = cp_model.CpSolver()
s.solve(m)

for i in range(4):
    print(f'Task {i}: {s.value(starts[i])} -> {s.value(ends[i])}')
print(f'Makespan: {s.value(makespan)}')

