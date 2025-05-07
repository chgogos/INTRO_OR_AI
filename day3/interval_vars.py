from ortools.sat.python import cp_model

model = cp_model.CpModel()

start_var = model.new_int_var(0, 100, "start")
length_var = model.new_int_var(10, 20, "length")
end_var = model.new_int_var(0, 100, "end")
is_present_var = model.new_bool_var("is_present")

# creating an interval whose length can be influenced by a variable (more expensive)
flexible_interval = model.new_interval_var(
    start=start_var, size=length_var, end=end_var, name="flexible_interval"
)

# creating an interval of fixed length
fixed_interval = model.new_fixed_size_interval_var(
    start=start_var,
    size=10,  # needs to be a constant
    name="fixed_interval",
)

# creating an interval that can be present or not and whose length can be influenced by a variable (most expensive)
optional_interval = model.new_optional_interval_var(
    start=start_var,
    size=length_var,
    end=end_var,
    is_present=is_present_var,
    name="optional_interval",
)

# creating an interval that can be present or not
optional_fixed_interval = model.new_optional_fixed_size_interval_var(
    start=start_var,
    size=10,  # needs to be a constant
    is_present=is_present_var,
    name="optional_fixed_interval",
)

