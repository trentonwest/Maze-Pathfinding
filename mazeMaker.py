import random

# Function to initialize the maze grid with walls
def initialize_maze(size):
    maze = [[2 for _ in range(size[0])] for _ in range(size[1])]
    return maze

# Function to check if a cell is within the maze boundaries
def is_valid_cell(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols

# Recursive Backtracking algorithm to generate the maze
def generate_maze(maze, x, y,size):
    rows,cols= size
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + 2 * dx, y + 2 * dy

        if is_valid_cell(nx, ny, rows, cols) and maze[nx][ny] == 2:
            maze[nx][ny] = 0  # Carve a passage
            maze[x + dx][y + dy] = 0  # Open the wall between cells
            generate_maze(maze, nx, ny,size)

def create_maze(size):
    width, height=size
    maze = [[2 for _ in range(width)] for _ in range(height)]  # Initialize maze with walls
    stack = [(0, 0)]
    maze[0][0] = 0

    while stack:
        x, y = stack[-1]
        neighbors = [(x, y-2), (x, y+2), (x-2, y), (x+2, y)]
        unvisited_neighbors = []
        for nx, ny in neighbors:
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 2:
                unvisited_neighbors.append((nx, ny))

        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)
            wall_x = (x + nx) // 2
            wall_y = (y + ny) // 2
            maze[wall_y][wall_x] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze
