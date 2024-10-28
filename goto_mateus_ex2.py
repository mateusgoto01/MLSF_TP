from constraint import Problem, ExactSumConstraint
from demineur import lectureGrille

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Résoudre le jeu du démineur avec la programmation par satisfaction de contraintes.
# Chaque cellule dont la valeur est inconnue est une variable dont le domaine est {0, 1},
# où 0 signifie « pas de mine » et 1 signifie « mine ».
# Nous définissons les cellules voisines à l'aide de la fonction get_neighbors, et la fonction has_non_zero_neighbor
# garantit que seules les cellules ayant un voisin numéroté sont considérées comme la variable.
# Pour chaque cellule numérotée, nous imposerons une restriction selon laquelle les valeurs de toutes les
# variables, des autres cellules (inconnues, ses cellules adjacentes) que nous introduirons s'élèvent à
# ce nombre, le nombre de mines. De cette manière, nous interdirons la production de solutions non valides.
# et chaque cellule inconnue pertinente contribue à une solution du tableau.
# du tableau.



# Function to get neighbors(everything around) of a position (row, column)
def get_neighbors(row, column, n):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_row, new_column = row + i, column + j
            if 0 <= new_row < n and 0 <= new_column < n:
                neighbors.append((new_row, new_column))
    return neighbors

def has_non_zero_neighbor(row, column, grid):
    neighbors = get_neighbors(row, column, len(grid))
    for r, c in neighbors:
        if grid[r][c] != 0:
            return True
    return False
# Function to solve Minesweeper using CSP using greedy method
def solve_minesweeper(n, grid):
    problem = Problem()

    # Create variables for all unknown cells (0s) with domain [0, 1]
    variables = {}
    for row in range(n):
        for column in range(n):
            if grid[row][column] == 0:
                #remove variables that dont have any numbered block close
                if (has_non_zero_neighbor(row, column, grid)):        
                    variables[(row, column)] = (row, column)
                    problem.addVariable((row, column), [0, 1])  # 0: empty, 1: mine
    


    # Add constraints for cells with numbers (number of adjacent mines)
    for row in range(n):
        for column in range(n):
            if grid[row][column] > 0:
                neighbors = get_neighbors(row, column, n)
                unknown_neighbors = [v for v in neighbors if (v[0], v[1]) in variables]
                
                # Adds constraint: the sum of mines in the neighbors must equal the number in the cell
                problem.addConstraint(ExactSumConstraint(grid[row][column]), unknown_neighbors)

    # Solve the CSP
    solution = problem.getSolutions()
    return solution

# Function to display the solution in a readable form
def display_solution_graphically(n, grid, solution, title):
    # Create a grid of zeros
    matrix = np.zeros((n, n))

    # Fill the matrix with the values from the grid
    for row in range(n):
        for column in range(n):
            if grid[row][column] > 0:
                matrix[row, column] = grid[row][column]  # Numbers
            elif (row, column) in solution and solution[(row, column)] == 1:
                matrix[row, column] = -1  # Marks the mine with -1

    # Create the graph
    fig, ax = plt.subplots(figsize=(8, 8))  # Adjust the figure size if necessary
    ax.set_xticks(np.arange(n + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(n + 1) - 0.5, minor=True)

    # Set the background to light blue
    ax.set_facecolor('white')  # Light blue
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2, alpha=0.7)  # Grid lines

    # Plot the numbers and mines
    for row in range(n):
        for column in range(n):
            if matrix[row, column] > 0:  # Numbers
                ax.text(column, row, str(int(matrix[row, column])), 
                        ha='center', va='center', fontsize=12)
            elif matrix[row, column] == -1:  # Mine
                mine_img = plt.imread('bomb.png')  
                imagebox = OffsetImage(mine_img, zoom=0.05)  
                ab = AnnotationBbox(imagebox, (column, row), frameon=False)
                ax.add_artist(ab)

    # Final graph settings
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)  # Invert the y-axis so that (0, 0) is at the top left corner (avoid problem with organization of the grid)
    plt.title(title, fontsize=14)

#for each grille we have:
n, _, grid = lectureGrille(r'grille/grille1.txt')
solutions = solve_minesweeper(n, grid)
print("solution len:", len(solutions))
display_solution_graphically(n, grid, solutions[0], "Démineur 1")

n, _, grid = lectureGrille(r'grille/grille2.txt')
solutions = solve_minesweeper(n, grid)
print("solution len:", len(solutions))
display_solution_graphically(n, grid, solutions[0], "Démineur 2")

n, _, grid = lectureGrille(r'grille/grille3.txt')
solutions = solve_minesweeper(n, grid)
print("solution len:", len(solutions))
display_solution_graphically(n, grid, solutions[0], "Démineur 3")
plt.show()