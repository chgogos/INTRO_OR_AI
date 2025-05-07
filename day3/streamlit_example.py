import streamlit as st
import matplotlib.pylab as plt
from ortools.sat.python import cp_model

def solve():
    # create model
    model = cp_model.CpModel()
    
    # decision variables
    x1 = model.new_int_var(0,10_000, "x1")
    x2 = model.new_int_var(0,10_000, "x2")
    
    model.add(3*x1 + 5*x2 <= 3600) # wood
    model.add(x1 + 2*x2 <= 1600) # labor (hours)
    model.add(50*x1 + 20*x2 <= 48000) # machine time (minutes)
    
    model.maximize(desk_price*x1+table_price*x2)
    
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    if status == cp_model.OPTIMAL:
        return solver.objective_value, solver.value(x1), solver.value(x2)

st.title("A product mix problem")
st.write("Our company produces desks and tables")
st.write("Production of one desk requires 3 units of wood, 1 hour of labor and 50 minutes of machine time")
st.write("We have 3600 units of wood, 1600 labour hours and 48000 minutes of machine time")
desk_price = st.slider('Desks unit price', min_value=500, max_value=1500, step=10, value=700)
table_price = st.slider('Tables unit price', min_value=500, max_value=1500, step=10, value=900)
st.write(f"desk price={desk_price} \u20AC, table price={table_price} \u20AC")
    
objective, desk_items, table_items = solve()

st.markdown("---")
st.markdown("## Results")
st.write(f"Total profit = {objective:.0f} \u20AC")
st.write(f"Number of desks = **{desk_items}**, Number of tables = **{table_items}**")

st.markdown("---")
fig, ax = plt.subplots()
ax.bar(["Desks", "Tables"], [desk_items, table_items], color=["blue", "orange"])
ax.set_ylabel("Number of items")
ax.set_title("Production Mix")
for i, v in enumerate([desk_items, table_items]):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
st.pyplot(fig)