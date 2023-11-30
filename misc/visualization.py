import pygame
import sys
import tools.datamanagement as datamanagement
import numpy as np
#availability_matrix =datamanagement.load_object("/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/availability_matrix.pickle")
availability_matrix=np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]
 ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
 ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
 ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
 ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
 ,[0, 0, 0, 0, 1, 0, 0, 1, 0]
 ,[0, 0, 0, 0, 1, 0, 0, 1, 0]
 ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
 ,[0, 0, 0, 0, 1, 0, 1, 0, 0]
 ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
 ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
 ,[0, 1, 1, 1, 1, 1, 1, 1, 0]
 ,[0, 1, 1, 0, 1, 0, 0, 0, 0]
 ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
 ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
 ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
 ,[0, 0, 0, 0, 0, 0, 0, 0, 0]])
# Initialize Pygame
pygame.init()
print(availability_matrix)

# Constants
GRID_SIZE = 20

WIDTH, HEIGHT = GRID_SIZE * availability_matrix.shape[0], GRID_SIZE * availability_matrix.shape[1]
CHARACTER_SIZE = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid World")

# Initialize grid
grid = [[WHITE for _ in range(WIDTH // GRID_SIZE)] for _ in range(HEIGHT // GRID_SIZE)]

# Initialize character
character_x, character_y = GRID_SIZE, 7 * GRID_SIZE
character_speed = GRID_SIZE
policy = ["up", "right","up","up","right","right","right","right","right","right","right","right","right", "up","up","right","right","right","right","up"]
current_action = 0

# Add targets and obstacles to the grid
grid[1][15] = GREEN  # Example target cell
grid[7][10] = BLACK  # Example obstacle cell
for x in range(availability_matrix.shape[0]):
    for y in range(availability_matrix.shape[1]):
        if not availability_matrix[x, y]:
            #print(availability_matrix[x, y])
            grid[y][x] = BLACK

# Game loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Perform action from the array
                if policy[current_action] == "up":
                    character_y -= character_speed
                elif policy[current_action] == "down":
                    character_y += character_speed
                elif policy[current_action] == "left":
                    character_x -= character_speed
                elif policy[current_action] == "right":
                    character_x += character_speed

                current_action = (current_action + 1) % len(policy)

    # Draw grid with outlines
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(screen, grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Draw character
    pygame.draw.rect(screen, BLUE, (character_x, character_y, CHARACTER_SIZE, CHARACTER_SIZE))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
