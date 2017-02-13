# Code is derived from examples and solutions given in class. My main changes are clearly marked, otherwise they are a combo of Udacity's and mine solution from the regular sudoku problem

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

assignments = []
values = []
all_digits = '123456789'

# Row/Col Names
rows = 'ABCDEFGHI'
cols = all_digits


boxes = cross(rows, cols)

# Units on the board
# Rows in Board
row_units = [cross(r, cols) for r in rows]

# Columns in Board
col_units = [cross(rows, c) for c in cols]

# 3x3 Squares in Board
square_units = [cross(row_set, cols_set)
                for row_set in ('ABC', 'DEF', 'GHI')
                for cols_set in ('123', '456', '789')]

# Diagonal Units in Board, example: [A1, B2, C3, D4, ... I9] by Melanie
diag_units = [[x + y for x, y in zip(rows, cols)],  [x + y for x, y in zip(rows, reversed(cols))]]

# Unit list for normal suduko by Melanie
unitlist = row_units + col_units + square_units + diag_units

# Creates units and peers from the UnitList, taken from example code in lesson
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.

    Author:
        Melanie Burns
    """

    # Go through every box and each of that boxes peers
    for box in values.keys():
        for peer in peers[box]:

            # Find if they are twins
            if values[box] == values[peer] and len(values[box]) == 2 and len(values[peer]) == 2:

                # Find all shared units
                for box_units in units[box]:
                    if box_units in units[peer]:

                        # Elimate both twins from that unit
                        for x in box_units:
                            if x != box and x != peer:
                                values[x] = values[x].replace(values[box][0], '')
                                values[x] = values[x].replace(values[box][1], '')

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    # Check that the grid is the correct length, otherwise raise an exception
    if len(grid) != 81:
        raise ValueError("Grid must be 81 boxes")

    # Change the empty spaces to all options, and build the board
    grid = [x if x != '.' else all_digits for x in grid]
    values = dict(zip(boxes, grid))

    # TODO: update to use pygame
    #values = [assign_value(values, b, x) if x != '.' else '123456789' for b,x in zip(boxes, grid) ]
    return values

# Took this code directly from the example code in the lesson. No reason to change it.
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    # Find each box that has been solved
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        solution = values[box]
        # Peers in the Utils
        for peer in peers[box]:
            values[peer] = values[peer].replace(solution, '')

    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # Use the unit list from util
    for unit in unitlist:
        # Count from 1 to 9
        for digit in all_digits:
            # Find all the all the potential boxes within that unit
            potential_solutions = [box for box in unit if digit in values[box]]
            # If its the only choice than add replace other options with it
            if len(potential_solutions) == 1:
                values[potential_solutions[0]] = digit

    return values

def reduce_puzzle(values):
    """
       Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
       If the sudoku is solved, return the sudoku.
       If after an iteration of both functions, the sudoku remains the same, return the sudoku.
       Input: A sudoku in dictionary form.
       Output: The resulting sudoku in dictionary form.
       """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate and Only Choice Strategies
        values = eliminate(values)
        values = only_choice(values)

        # Originally I thought you wanted me to solve diagonal with the twins, I'm leaving this here as it is how you would solve it the rest of the way
        #values = naked_twins(values)
        #values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
       Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
       Input: A sudoku in dictionary form.
       Output: The resulting sudoku in dictionary form.
    """
    # Using depth-first search and propagation, create a search tree and solve the sudoku.
    values = reduce_puzzle(values)

    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s)
                for s in boxes
                if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    Author:
        Melanie Burns
    """
    # Create a dictionary of values from the grid
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

