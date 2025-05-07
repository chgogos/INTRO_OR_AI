from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, letter_vars, word1, word2, result_word):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.letter_vars = letter_vars
        self.word1 = word1
        self.word2 = word2
        self.result_word = result_word
        self.solution_count = 0

    def OnSolutionCallback(self):
        self.solution_count += 1
        assignment = {l: self.Value(var) for l, var in self.letter_vars.items()}
        w1_val = sum(
            assignment[l] * (10**i) for i, l in enumerate(reversed(self.word1))
        )
        w2_val = sum(
            assignment[l] * (10**i) for i, l in enumerate(reversed(self.word2))
        )
        res_val = sum(
            assignment[l] * (10**i) for i, l in enumerate(reversed(self.result_word))
        )
        print(
            f"{self.word1} ({w1_val}) - {self.word2} ({w2_val}) = {self.result_word} ({res_val})"
        )
        print("Assignment:", assignment)
        print()


# Function to map a word to its numeric expression given letter variables
def word_to_number(word, letter_vars):
    return sum(letter_vars[letter] * (10**i) for i, letter in enumerate(reversed(word)))


def solve_word_equation(word1, word2, result_word):
    model = cp_model.CpModel()

    # Get unique letters
    unique_letters = sorted(set(word1 + word2 + result_word))
    if len(unique_letters) > 10:
        raise ValueError("Too many unique letters (more than 10)")

    # Create variables for each letter
    letter_vars = {letter: model.new_int_var(0, 9, letter) for letter in unique_letters}

    # All letters must be assigned different digits
    model.add_all_different(letter_vars.values())

    # Leading letters cannot be zero
    for word in [word1, word2, result_word]:
        model.add(letter_vars[word[0]] != 0)

    # Map words to numbers
    word1_num = word_to_number(word1, letter_vars)
    word2_num = word_to_number(word2, letter_vars)
    result_num = word_to_number(result_word, letter_vars)

    # Constraint: word1 - word2 == result
    model.add(word1_num - word2_num == result_num)

    # Create solver
    solver = cp_model.CpSolver()

    printer = SolutionPrinter(letter_vars, word1, word2, result_word)
    solver.solve(model, printer)

    if printer.solution_count == 0:
        print("No solution found.")


# Example run
solve_word_equation("NINE", "FOUR", "FIVE")
