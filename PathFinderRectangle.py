import pygame
import time
import heapq
import sys
import mazeMaker
import copy

pygame.init()

def get_color(val):
    if val == 0:
        return (0,0,0)
    elif val == 1:
        return (255,0,0)
    elif val == 2:
        return (255,255,255)
    elif val == 3:
        return (0,255,0)

    return (val%255,val//2 %220,255-val%255)

def draw_box(x,y):
    color = get_color(board[x][y])
    if board[x][y]!=2:
        pygame.draw.rect(window, (0,0,0), (y*box_size, x*box_size, box_size, box_size))  # (x, y, width, height)
    pygame.draw.rect(window, color, (y*box_size+1, x*box_size+1, box_size-2, box_size-2))
    pygame.display.flip()
    #time.sleep(0.1)

def draw_board():
    for i in range(len(board)):
        for j in range(len(board[0])):
            pygame.draw.rect(window, (255,255,255), (j*box_size, i*box_size, box_size, box_size))  # (x, y, width, height)
            color = get_color(board[i][j])
            pygame.draw.rect(window, color, (j*box_size+1, i*box_size+1, box_size-2, box_size-2))
    pygame.display.flip()
    time.sleep(1.5)
    
# A STAR --------------------------------------------------------------------------------------
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def find_start_and_goal(matrix):
    rows, cols = len(matrix), len(matrix[0])
    start, goal = None, None
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                if start is None:
                    start = (i, j)
                else:
                    goal = (i, j)
                    return start, goal
    return None, None

def astar(matrix,touched):
    start, goal = find_start_and_goal(matrix)
    rows, cols = len(matrix), len(matrix[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_scores = {start: 0}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            print(f'A-Star checked {len(touched)} boxes')
            return list(path)
        
        for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x,y= current[0] + i, current[1] + j
            neighbor =x,y
            if 0 <= x < rows and 0 <= y < cols and matrix[x][y] != 2:
                tentative_g_score = g_scores[current] + 1
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))
                touched.append((x,y))
                board[x][y]=int(tentative_g_score)+5
                draw_box(x,y)
    print('no path')
    return None  # No path found

def do_aStar():
    touched=[]
    path=astar(board,touched)

    #remove last element, flip it to remove the first element too, keeping the start and finish not in the solution
    path.pop(0)     
    #draw path
    for x,y in path:
        board[x][y]=3
        draw_box(x,y)

# Dykstra --------------------------------------------------------------------------------------
def dijkstra(maze,touched):
    rows, cols = len(maze), len(maze[0])
    start, end = None, None
    
    # Find start and end points in the maze
    start, end = find_start_and_goal(maze)
    
    if start is None or end is None:
        raise ValueError("Start and/or end points not found in the maze.")
    
    # Directions for moving: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Initialize distances with infinity for all cells except the start cell
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = 0
    
    # Predecessors dictionary to keep track of the predecessors of each cell
    predecessors = {}
    
    # Priority queue for Dijkstra's algorithm: (distance, cell)
    pq = [(0, start)]
    while pq:
        current_distance, current_cell = heapq.heappop(pq)
        
        # If reached the end point, reconstruct the path and return it
        if current_cell == end:
            path = []
            while current_cell in predecessors:
                path.insert(0, current_cell)
                current_cell = predecessors[current_cell]
            path.insert(0,start)
            print(f'Dijkstra checked {len(touched)} boxes')
            return path
        
        for direction in directions:
            dx, dy = direction
            new_x, new_y = current_cell[0] + dx, current_cell[1] + dy
            
            # Check if the new cell is within the maze and not a wall (value 2)
            if 0 <= new_x < rows and 0 <= new_y < cols and maze[new_x][new_y] != 2:
                # Calculate new distance
                new_distance = current_distance + 1
                
                # If the new distance is shorter, update the distance, add the cell to the priority queue,
                # and update the predecessor for the new cell
                if new_distance < distances[new_x][new_y]:
                    distances[new_x][new_y] = new_distance
                    heapq.heappush(pq, (new_distance, (new_x, new_y)))
                    predecessors[(new_x, new_y)] = current_cell
                touched.append((new_x,new_y))
                board[new_x][new_y]=int(new_distance)+5
                draw_box(new_x,new_y)

    # If the end point is not reachable from the start point, return an empty path
    return []

def do_dijk():
    touched=[]
    path=dijkstra(board,touched)

    #remove last element, flip it to remove the first element too, keeping the start and finish not in the solution
    path.pop(0)     
    path.reverse()
    path.pop(0)

    #draw path
    for x,y in path:
        board[x][y]=3
        draw_box(x,y)
        #time.sleep(0.03)

# RHR -------------------------------------------------------------------------------------- 
def is_valid_move(maze, x, y):
    if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] in [0, 1]:
        return True
    return False

def RHR(maze, x, y,count):
    if maze[x][y] == 1:
        print(f'RHR checked {count} boxes')
        return [(x, y)]  # Reached the finish line
    
    if is_valid_move(maze, x, y):
        maze[x][y] = count  # Mark the cell as visited
        count+=1
        draw_box(x,y)
        # Explore in all possible directions: up, down, left, right
        if RHR(maze, x+1, y,count):
            return [(x, y)] + RHR(maze, x+1, y,count)
        elif RHR(maze, x-1, y,count):
            return [(x, y)] + RHR(maze, x-1, y,count)
        elif RHR(maze, x, y+1,count):
            return [(x, y)] + RHR(maze, x, y+1,count)
        elif RHR(maze, x, y-1,count):
            return [(x, y)] + RHR(maze, x, y-1,count)
        
        # If no valid path is found, backtrack
        maze[x][y] = 2  # Mark the cell as a wall
        draw_box(x,y)
        return []
    
    return []

def do_RHR():
    start,end=find_start_and_goal(board)
    board[0][0]=0
    draw_box(0,0)
    count=10
    RHR(board,start[0],start[1],count)

# Depth 1st -------------------------------------------------------------------------------------- 
def dfs(maze, start, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    x, y = start
    if maze[x][y] == 1:
        # Reached the finish
        count=0
        for value in visited:
            if value:
                count+=1
        print(f'DFS checked {count} boxes')
        path.append((x, y))
        return path
    
    if maze[x][y] == 2 or (x, y) in visited:
        # Hit a wall or already visited this cell
        return None
    
    visited.add((x, y))
    
    # Explore neighbors in DFS manner: down, right, up, left
    neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    for neighbor in neighbors:
        if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]):
            result = dfs(maze, neighbor, visited, path)
            if result:
                board[x][y]=len(path)+5
                draw_box(x,y)
                path.append((x, y))
                return path
    
    return None

def do_dfs():
    board[0][0]=0
    dfs(board,(0,0))


#__________________________INITIALIZATION OF BOARD AND SCREEN______________________________
#set up window       
window_width, window_height = 2000,1000
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Path Finder")

box_size = 10
grid_size= window_width//box_size,window_height//box_size


#make maze
sys.setrecursionlimit(100000)
#board = mazeMaker.initialize_maze(grid_size)
#mazeMaker.generate_maze(board, 0, 0,grid_size)
board=mazeMaker.create_maze(grid_size)

#make start and finish
board[0][0]=1
board[len(board)-2][len(board[0])-2]=1

#copy the board to reset it after each algo
blank=copy.deepcopy(board)

draw_board()
#________________________________________________________

#do a star
do_aStar()
time.sleep(1.5)
board=copy.deepcopy(blank)
draw_board()

#do dijkstra
do_dijk()
time.sleep(1.5)
board=copy.deepcopy(blank)
draw_board()

#do right hand rule
do_RHR()
time.sleep(1.5)
board=copy.deepcopy(blank)
draw_board()

# do depth first search
do_dfs()
time.sleep(1.5)
board=copy.deepcopy(blank)
draw_board()

