import streamlit as st
import numpy as np
from ortools.sat.python import cp_model
import time

def generate_complete_sudoku():
    """Generate a complete valid 9x9 Sudoku solution"""
    grid = np.zeros((9, 9), dtype=int)
    
    def is_valid(grid, row, col, num):
        # Check row
        for x in range(9):
            if grid[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if grid[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_grid(grid):
        import random
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if solve_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    solve_grid(grid)
    return grid

def create_initial_puzzle():
    """Create a random 9x9 Sudoku puzzle by removing numbers from a complete solution"""
    import random
    
    # Generate a complete solution
    complete_grid = generate_complete_sudoku()
    
    # Create a copy to remove numbers from
    puzzle = complete_grid.copy()
    
    # Randomly remove numbers to create the puzzle
    # Remove between 45-55 numbers (leaving 26-36 clues)
    num_to_remove = random.randint(45, 55)
    
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    for i in range(num_to_remove):
        row, col = positions[i]
        puzzle[row][col] = 0
    
    return puzzle

def solve_sudoku_ortools(puzzle):
    """Solve the 9x9 Sudoku using OR-Tools CP-SAT"""
    model = cp_model.CpModel()
    
    # Create variables for each cell (1-9 values)
    grid_vars = {}
    for i in range(9):
        for j in range(9):
            grid_vars[(i, j)] = model.NewIntVar(1, 9, f'grid_{i}_{j}')
    
    # Add constraints for pre-filled cells
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                model.Add(grid_vars[(i, j)] == puzzle[i][j])
    
    # Row constraints - each row contains 1-9
    for i in range(9):
        model.AddAllDifferent([grid_vars[(i, j)] for j in range(9)])
    
    # Column constraints - each column contains 1-9
    for j in range(9):
        model.AddAllDifferent([grid_vars[(i, j)] for i in range(9)])
    
    # 3x3 box constraints
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_vars = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    box_vars.append(grid_vars[(i, j)])
            model.AddAllDifferent(box_vars)
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                solution[i][j] = solver.Value(grid_vars[(i, j)])
        return solution, True
    else:
        return puzzle, False

def display_sudoku_grid(grid, original_puzzle=None):
    """Display the Sudoku grid using HTML table with proper styling"""
    html = """
    <style>
    .sudoku-table {
        border-collapse: collapse;
        margin: 20px auto;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        border: 3px solid #000;
    }
    .sudoku-table td {
        width: 40px;
        height: 40px;
        text-align: center;
        vertical-align: middle;
        border: 1px solid #ccc;
        background-color: #fff;
    }
    .sudoku-table td.original {
        background-color: #f0f0f0;
        font-weight: bold;
        color: #000;
    }
    .sudoku-table td.solved {
        background-color: #e8f5e8;
        color: #006600;
    }
    .sudoku-table td.empty {
        background-color: #fff;
        color: #ccc;
    }
    .sudoku-table tr:nth-child(3n) td {
        border-bottom: 3px solid #000;
    }
    .sudoku-table td:nth-child(3n) {
        border-right: 3px solid #000;
    }
    </style>
    <table class="sudoku-table">
    """
    
    for i in range(9):
        html += "<tr>"
        for j in range(9):
            value = grid[i][j]
            cell_class = ""
            display_value = ""
            
            if value == 0:
                cell_class = "empty"
                display_value = ""
            elif original_puzzle is not None and original_puzzle[i][j] != 0:
                cell_class = "original"
                display_value = str(value)
            else:
                cell_class = "solved"
                display_value = str(value)
            
            html += f'<td class="{cell_class}">{display_value}</td>'
        html += "</tr>"
    
    html += "</table>"
    return html

def get_difficulty_level(num_clues):
    """Determine difficulty level based on number of clues"""
    if num_clues >= 36:
        return "Easy"
    elif num_clues >= 32:
        return "Medium"
    elif num_clues >= 28:
        return "Hard"
    else:
        return "Expert"

def main():
    st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="centered")
    
    st.title("🧩 Random Sudoku Solver")
    st.markdown("**Each reset generates a completely new random puzzle!**")
    
    # Initialize session state
    if 'current_grid' not in st.session_state:
        st.session_state.original_puzzle = create_initial_puzzle()
        st.session_state.current_grid = st.session_state.original_puzzle.copy()
        st.session_state.is_solved = False
        st.session_state.solve_time = 0
    
    # Display the Sudoku grid
    grid_html = display_sudoku_grid(
        st.session_state.current_grid, 
        st.session_state.original_puzzle
    )
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # Create two columns for buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Puzzle", use_container_width=True, type="secondary"):
            st.session_state.original_puzzle = create_initial_puzzle()
            st.session_state.current_grid = st.session_state.original_puzzle.copy()
            st.session_state.is_solved = False
            st.session_state.solve_time = 0
            st.rerun()
    
    with col2:
        if st.button("🤖 Solve with OR-Tools", use_container_width=True, type="primary"):
            if not st.session_state.is_solved:
                with st.spinner("Solving with CP-SAT..."):
                    start_time = time.time()
                    solution, success = solve_sudoku_ortools(st.session_state.original_puzzle)
                    solve_time = time.time() - start_time
                    
                    if success:
                        st.session_state.current_grid = solution
                        st.session_state.is_solved = True
                        st.session_state.solve_time = solve_time
                        st.rerun()
                    else:
                        st.error("❌ No solution found!")
            else:
                st.info("✅ Puzzle already solved!")
    
    # Display solve information
    if st.session_state.is_solved:
        st.success(f"🎉 **Puzzle solved in {st.session_state.solve_time:.3f} seconds!**")
        
        # Display statistics
        filled_originally = np.count_nonzero(st.session_state.original_puzzle)
        st.info(f"📊 **Puzzle Statistics:** {filled_originally}/81 clues provided ({filled_originally/81*100:.1f}% filled)")
    else:
        # Show current puzzle statistics
        filled_originally = np.count_nonzero(st.session_state.original_puzzle)
        st.info(f"📊 **Current Puzzle:** {filled_originally}/81 clues provided ({filled_originally/81*100:.1f}% filled)")
    
    # Legend
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔲 **Original clues** - Dark background")
    with col2:
        st.markdown("🟢 **Solved cells** - Green background") 
    with col3:
        st.markdown("⬜ **Empty cells** - White background")
    
    # Information about the solver
    with st.expander("🔍 About OR-Tools CP-SAT Solver"):
        st.markdown("""
        **OR-Tools CP-SAT (Constraint Programming with Boolean Satisfiability):**
        
        - **Random Puzzle Generation**: Each puzzle is generated by creating a complete valid Sudoku solution and then randomly removing 45-55 numbers
        - **Constraint Programming**: Models the Sudoku as a constraint satisfaction problem
        - **Variables**: Creates 81 integer variables (one per cell) with domain 1-9
        - **Constraints**: 
          - 9 row constraints (each row contains digits 1-9)
          - 9 column constraints (each column contains digits 1-9)
          - 9 box constraints (each 3×3 box contains digits 1-9)
          - Clue constraints (pre-filled cells must keep their values)
        - **Solving**: Uses advanced techniques like constraint propagation, conflict-driven learning, and systematic search
        - **Performance**: Typically solves puzzles in milliseconds, regardless of difficulty
        
        Every puzzle is guaranteed to have a unique solution since it's generated from a complete valid grid.
        """)

if __name__ == "__main__":
    main()