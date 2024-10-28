from constraint import *

def lectureGrille(filename):
    with open(filename, mode='r') as file:
        lines = int(file.readline())
        cols = int(file.readline())
        grid = [[0]*cols for i in range(lines)]
        for i in range(lines):
            line = file.readline()
            for j in range(cols):
                if line[j]!='0':
                    grid[i][j] = int(line[j])
        return (lines, cols, grid)

if __name__ == "__main__":
    lines, cols, grille = lectureGrille(r'grille/grille1.txt')
    print(lines)