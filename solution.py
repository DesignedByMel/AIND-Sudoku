def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

assignments = []

# Row/Col Names
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

# make units
# collumns, rows, squares, diagonals <- that should solve the second problem
# Rows in Board
row_units = [cross(r, cols) for r in rows]

# Collumns in Board
cols_units = [cross(rows, c) for c in cols]

# 3x3 Squares in Board
square_units = [cross(row_set, cols_set)
                for row_set in ('ABC', 'DEF', 'GHI')
                for cols_set in ('123', '456', '789')]

# Unit list for normal suduko
unitlist = row_units + col_units + square_units

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
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers





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

    if len(grid) != 81:
        raise ValueError("Grid must be 81 boxes")

    grid = [x if x != '.' else '12346789' for x in grid]
    values = dict(zip(boxes, grid))

    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass


def eliminate(values):
    pass


def only_choice(values):
    pass


def reduce_puzzle(values):
    pass


def search(values):
    pass


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Board encoding


    # Create a dictionary of values from the grid
    values = grid_values(grid)
    print(values)
    return values


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


 # 2 Diagonals in Board
    #diag_units = [x + y for x, y in zip(rows, cols) ]