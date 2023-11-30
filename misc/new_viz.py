import pygame
import sys
import numpy as np
import pbvi as pvbi
from scipy.special import softmax
from collections import namedtuple

# Function to load the availability matrix
def load_availability_matrix(file_path):
    # Implement your loading logic here
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
    return availability_matrix
availability_matrix = load_availability_matrix("path")
# Define the transition model, observation model, and reward model
def transition_model(state, action):
    # Placeholder transition model
    # Assuming 80% success and 20% failure
    if np.random.rand() < 0.8:
        next_state = np.array(state)  # No movement on failure
    else:
        next_state = np.array(state)
        if action == "up" and state[1] > 0:
            next_state[1] -= 1
        elif action == "down" and state[1] < availability_matrix.shape[1] - 1:
            next_state[1] += 1
        elif action == "left" and state[0] > 0:
            next_state[0] -= 1
        elif action == "right" and state[0] < availability_matrix.shape[0] - 1:
            next_state[0] += 1
    return tuple(next_state)

def observation_model(state, action, next_state):
    # Placeholder observation model
    return softmax(np.random.rand(4))  # Example: Random probabilities for observations

def reward_model(state, action):
    # Placeholder reward model
    if action in ["up", "down", "left", "right"]:
        return -0.1  # Penalty for movement
    elif state == (1, 15):
        return 10.0  # Reward for reaching the target
    else:
        return 0.0  # No reward otherwise

# Define PBVI class
class PygamePBVI(pvbi.PBVI):
    def __init__(self, T, Omega, R, gamma, goal_state):
        super().__init__(T, Omega, R, gamma)
        self.goal_state = goal_state

    def transition_model(self, state, action):
        # Placeholder transition model
        if np.random.rand() < 0.8:
            next_state = np.array(state)  # No movement on failure
        else:
            next_state = np.array(state)
            if action == "up" and state[1] > 0:
                next_state[1] -= 1
            elif action == "down" and state[1] < availability_matrix.shape[1] - 1:
                next_state[1] += 1
            elif action == "left" and state[0] > 0:
                next_state[0] -= 1
            elif action == "right" and state[0] < availability_matrix.shape[0] - 1:
                next_state[0] += 1
        return tuple(next_state)

    def observation_model(self, state, action, next_state):
        # Placeholder observation model
        return softmax(np.random.rand(4))  # Example: Random probabilities for observations

    def reward_model(self, state, action):
        # Placeholder reward model
        if action in ["up", "down", "left", "right"]:
            return -0.1  # Penalty for movement
        elif state == (1, 15):
            return 10.0  # Reward for reaching the target
        else:
            return 0.0  # No reward otherwise

    def is_goal_state(self, state):
        # Check if the current state is the goal state
        return tuple(state) == self.goal_state

# Load the availability matrix
# availability_matrix = load_availability_matrix("/path/to/your/availability_matrix.pickle")

# availability_matrix=np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]
# ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
# ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
# ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
# ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
# ,[0, 0, 0, 0, 1, 0, 0, 1, 0]
# ,[0, 0, 0, 0, 1, 0, 0, 1, 0]
# ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
# ,[0, 0, 0, 0, 1, 0, 1, 0, 0]
# ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
# ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
# ,[0, 1, 1, 1, 1, 1, 1, 1, 0]
# ,[0, 1, 1, 0, 1, 0, 0, 0, 0]
# ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
# ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
# ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
# ,[0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20
WIDTH, HEIGHT = GRID_SIZE * availability_matrix.shape[0], GRID_SIZE * availability_matrix.shape[1]
CHARACTER_SIZE = 20
FPS = 60
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

# Initialize PygamePBVI
goal_state = (1, 15)  # Example: Goal at the top-left corner
pbvi_instance = PygamePBVI(T=transition_model, Omega=observation_model, R=reward_model, gamma=0.9, goal_state=goal_state)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Perform PBVI iteration
    V, best_actions = pbvi_instance.V(Epsi, B)
    B = pbvi_instance.expanded_B(B)

    # Choose the best action based on the current belief state
    current_belief_state = np.array([character_x // GRID_SIZE, character_y // GRID_SIZE])
    current_action = best_actions[np.argmax(np.dot(V, current_belief_state))]

    # Perform the chosen action
    if current_action == "up" and character_y > 0:
        character_y -= character_speed
    elif current_action == "down" and character_y < HEIGHT - CHARACTER_SIZE:
        character_y += character_speed
    elif current_action == "left" and character_x > 0:
        character_x -= character_speed
    elif current_action == "right" and character_x < WIDTH - CHARACTER_SIZE:
        character_x += character_speed

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
